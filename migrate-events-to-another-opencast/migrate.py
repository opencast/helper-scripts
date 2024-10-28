#!/usr/bin/env python3

import json

import lxml.etree as le
import urllib3
import MySQLdb
import sys

SOURCE_HOST_ADMIN = 'https://source-admin.opencast.org'
SOURCE_HOST_PRESENTATION = 'https://source-presentation.opencast.org'
SOURCE_USER = 'admin'
SOURCE_PASS = 'opencast'
SOURCE_SERIES_NAMES = []

SOURCE_DB_HOST = '127.0.0.1'
SOURCE_DB_PORT = 3306
SOURCE_DB_USER = 'admin'
SOURCE_DB_PASSWORD = 'opencast'
SOURCE_DB_DATABASE = 'opencast'

TARGET_HOST = 'https://target.opencast.org'
TARGET_USER = 'admin'
TARGET_PASS = 'opencast'
TARGET_WORKFLOW = 'import'

ONLY_SMALL_VIDEO_TRACKS = False


http = urllib3.PoolManager()

try:
    database = MySQLdb.connect(
        user=SOURCE_DB_USER,
        password=SOURCE_DB_PASSWORD,
        host=SOURCE_DB_HOST,
        port=SOURCE_DB_PORT,
        database=SOURCE_DB_DATABASE
    )
    cursor = database.cursor()
except MySQLdb.Error as e:
    print(f"Error connecting to Database: {e}")
    sys.exit(1)


def get_published_series(series_name=None):
    '''
    Generator, requesting all published media packages from the search service
    of the source Opencast. The media packages hold links to all published
    media and can be passed on as-is to the target Opencast.

    :param series_name: Name of series to be searched
    :return: Triple of series Dublin Core XML, ACL XML and series id
    '''
    url_search = f'{SOURCE_HOST_PRESENTATION}/search/series.json'
    headers = urllib3.make_headers(basic_auth=f'{SOURCE_USER}:{SOURCE_PASS}')

    offset = 0
    total = 1
    limit = 2

    # get published media packages from source opencast
    while total > offset:
        fields = {
            'limit': limit,
            'offset': offset
        }

        # Search for series by free-text query
        if series_name:
            fields['q'] = series_name

        request = http.request('GET', url_search, headers=headers, fields=fields)
        data = request.data.decode('utf-8')
        data = json.loads(data)

        offset = data.get('offset') + limit
        total = data.get('total')
        results = data.get('result', [])
        if type(results) is not list:
            results = [results]

        for result in results:
            dc = result.get('dc', {})
            series_id = dc.get('identifier')[0]
            print('Importing', series_id)

            # get dublin core
            url_dc = f'{SOURCE_HOST_ADMIN}/series/{series_id}.xml'
            request = http.request('GET', url_dc, headers=headers)
            dublincore = request.data.decode('utf-8').strip()

            # get acl
            url_acl = f'{SOURCE_HOST_ADMIN}/series/{series_id}/acl.xml'
            request = http.request('GET', url_acl, headers=headers)
            acl = request.data.decode('utf-8').strip()

            yield dublincore, acl, series_id


def create_series(dublincore, acl):
    '''
    Creates a series with given metadata and access control rules in the target
    Opencast.

    :param dublincore: Dublin Core metadata XML
    :type dublincore: str
    :param acl: Access control list as XML
    :type acl: str
    '''
    url_series = f'{TARGET_HOST}/series/'
    headers = urllib3.make_headers(basic_auth=f'{TARGET_USER}:{TARGET_PASS}')

    request = http.request('POST', url_series, headers=headers, fields={
        'series': dublincore,
        'acl': acl})
    print('Create series response:', request.status)


def get_smallest_video_track_by_type(tracks):
    '''
    Searches the smallest video track for each track type. Tracks which do not contain a video will be ignored.

    :param tracks: List of tracks
    :return: Dictionary with keys for the type and values containing the smallest video track
    '''
    # Filter only video tracks
    # Ignore videos with mimetype = application/x-mpegURL as these can not always be processed by opencast
    tracks = filter(lambda track: 'video' in track and 'video' in track.get('mimetype'), tracks)

    smallest_video_tracks = {}
    for track in tracks:
        track_type = track.get('type')
        size = track.get('size')

        if track_type not in smallest_video_tracks or size < smallest_video_tracks[track_type].get('size'):
            smallest_video_tracks[track_type] = track

    return smallest_video_tracks


def remove_large_video_tracks_from_mediapackage(mediapackage, tracks):
    '''
    For each track type, removes all video tracks that are bigger than the smallest video track

    :param mediapackage: Media package as XML
    :param tracks: tracks as list used to find the smallest track
    :return: filtered media package as XML
    '''
    smallest_video_tracks = get_smallest_video_track_by_type(tracks)

    mediapackage = le.fromstring(bytes(mediapackage, encoding='utf-8'))
    media = mediapackage.find('{*}media')
    tracks = media.findall('{*}track')

    for track in tracks:
        track_id = track.get('id')
        track_type = track.get('type')
        video = track.find('{*}video')
        mimetype = track.find('{*}mimetype')

        # Remove useless hls playlists
        if mimetype.text == 'application/x-mpegURL':
            media.remove(track)

        # Ensure video exists, otherwise do not remove
        elif video is not None and 'video' in mimetype.text:
            # Remove bigger video track
            if track_type in smallest_video_tracks and smallest_video_tracks[track_type].get('id') != track_id:
                media.remove(track)

    return le.tostring(mediapackage, encoding='utf-8')


def get_published_media(series_id=None):
    '''
    Generator, requesting all published media packages from the search service
    of the source Opencast. The media packages hold links to all published
    media and can be passed on as-is to the target Opencast.

    :param series_id: series id to which the media belongs
    :return: Media package XML
    '''
    url_search = f'{SOURCE_HOST_PRESENTATION}/search/episode.json'
    headers = urllib3.make_headers(basic_auth=f'{SOURCE_USER}:{SOURCE_PASS}')

    offset = 0
    total = 1
    limit = 2

    # get published media packages from source opencast
    while total > offset:
        fields = {
            'limit': limit,
            'offset': offset
        }

        if series_id:
            fields['sid'] = series_id

        request = http.request('GET', url_search, headers=headers, fields=fields)
        data = request.data.decode('utf-8')
        data = json.loads(data)

        offset = data.get('offset') + limit
        total = data.get('total')
        results = data.get('result', [])

        if type(results) is not list:
            results = [results]

        for result in results:
            media_package = result.get('mediapackage', {})
            print('Importing ' + media_package.get('id'))

            print('Fetch mediapackage xml from database')
            cursor.execute('SELECT mediapackage_xml FROM oc_search WHERE id=%s', (media_package.get('id'),))
            mediapackage_xml = cursor.fetchone()[0]

            if ONLY_SMALL_VIDEO_TRACKS:
                media = media_package.get('media', {})
                tracks = media.get('track', [])

                if type(tracks) is not list:
                    tracks = [tracks]

                yield remove_large_video_tracks_from_mediapackage(mediapackage_xml, tracks)
            else:
                yield mediapackage_xml


def ingest(mediapackage):
    '''
    Takes a media package XML and ingests it to the target Opencast.

    :param mediapackage: Media package as XML
    :type mediapackage: str
    '''
    url_ingest = f'{TARGET_HOST}/ingest/ingest'
    headers = urllib3.make_headers(basic_auth=f'{TARGET_USER}:{TARGET_PASS}')

    request = http.request('POST', url_ingest, headers=headers, fields={
        'mediaPackage': mediapackage,
        'workflowDefinitionId': TARGET_WORKFLOW})
    print('Ingest response:', request.status)


def main():
    if SOURCE_SERIES_NAMES:
        # Collect only series and related medias by series names
        for series_name in SOURCE_SERIES_NAMES:
            for dublincore, acl, series_id in get_published_series(series_name):
                create_series(dublincore, acl)

                # Get series medias
                for mediapackage in get_published_media(series_id):
                    ingest(mediapackage)
    else:
        # Collect all series and medias
        for dublincore, acl in get_published_series():
            create_series(dublincore, acl)
        for mediapackage in get_published_media():
            ingest(mediapackage)


if __name__ == '__main__':
    main()
    database.close()
