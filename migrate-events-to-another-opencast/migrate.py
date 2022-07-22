#!/usr/bin/env python3

import json
import urllib3

SOURCE_HOST = 'https://source.opencast.org'
SOURCE_USER = 'admin'
SOURCE_PASS = 'opencast'

TARGET_HOST = 'https://target.opencast.org'
TARGET_USER = 'admin'
TARGET_PASS = 'opencast'
TARGET_WORKFLOW = 'import'


http = urllib3.PoolManager()


def get_published_series():
    '''
    Generator, requesting all published media packages from the search service
    of the source Opencast. The media packages hold links to all published
    media and can be passed on as-is to the target Opencast.

    :return: Tuple of series Dublin Core XML and ACL XML
    '''
    url_search = f'{SOURCE_HOST}/search/series.json'
    headers = urllib3.make_headers(basic_auth=f'{SOURCE_USER}:{SOURCE_PASS}')

    offset = 0
    total = 1
    limit = 2

    # get published media packages from source opencast
    while total > offset:
        request = http.request('GET', url_search, headers=headers, fields={
            'limit': limit,
            'offset': offset})
        data = request.data.decode('utf-8')
        data = json.loads(data).get('search-results')

        offset = data.get('offset') + limit
        total = data.get('total')
        results = data.get('result', [])
        if type(results) is not list:
            results = [results]

        for result in results:
            series_id = result.get('id')
            print('Importing', series_id)

            # get dublin core
            url_dc = f'{SOURCE_HOST}/series/{series_id}.xml'
            request = http.request('GET', url_dc, headers=headers)
            dublincore = request.data.decode('utf-8').strip()

            # get acl
            url_acl = f'{SOURCE_HOST}/series/{series_id}/acl.xml'
            request = http.request('GET', url_acl, headers=headers)
            acl = request.data.decode('utf-8').strip()

            yield (dublincore, acl)


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


def get_published_media():
    '''
    Generator, requesting all published media packages from the search service
    of the source Opencast. The media packages hold links to all published
    media and can be passed on as-is to the target Opencast.

    :return: Media package XML
    '''
    url_search = f'{SOURCE_HOST}/search/episode.json'
    headers = urllib3.make_headers(basic_auth=f'{SOURCE_USER}:{SOURCE_PASS}')

    offset = 0
    total = 1
    limit = 2

    # get published media packages from source opencast
    while total > offset:
        request = http.request('GET', url_search, headers=headers, fields={
            'limit': limit,
            'offset': offset})
        data = request.data.decode('utf-8')
        data = json.loads(data).get('search-results')

        offset = data.get('offset') + limit
        total = data.get('total')
        results = data.get('result', [])
        if type(results) is not list:
            results = [results]

        for result in results:
            print('Importing ' + result.get('id'))
            yield result.get('ocMediapackage')


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
    for dublincore, acl in get_published_series():
        create_series(dublincore, acl)

    for mediapackage in get_published_media():
        ingest(mediapackage)


if __name__ == '__main__':
    main()
