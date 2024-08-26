#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from json import dumps

from opencast.ingest import download_file, filename_from_url, remove_mediapackage_tmp_dir


def get_info_me(opencast_admin_client):
    url = '/api/info/me'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()


def get_series(opencast_admin_client, series_filter=None, series_sort='created:DESC', **kwargs):
    url = '/api/series'
    offset = 0
    batch_size = 20
    while offset >= 0:
        params = {
            'limit': batch_size,
            'offset': offset,
        }
        if series_filter:
            params['filter'] = series_filter
        if series_sort:
            params['sort'] = series_sort
        if kwargs:
            params |= kwargs
        response = opencast_admin_client.get(url, params=params)
        response.raise_for_status()
        for series_item in response.json():
            yield series_item
        if response.json():
            offset += batch_size
        else:
            offset = -1
            if offset == 0:
                return []


def get_specific_series(opencast_admin_client, series_id):
    url = f'/api/series/{series_id}'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()


def get_series_acl(opencast_admin_client, series_id):
    url = f'/api/series/{series_id}/acl'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()


def get_series_properties(opencast_admin_client, series_id):
    url = f'/api/series/{series_id}/properties'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()


def get_series_metadata(opencast_admin_client, series_id, catalog_type='dublincore/series'):
    url = f'/api/series/{series_id}/metadata'
    params = {
        'type': catalog_type,
    }
    response = opencast_admin_client.get(url, params=params)
    response.raise_for_status()
    return response.json()


def create_series(opencast_admin_client, metadata, acl, theme=None):
    url = '/api/series/'
    metadata_fields = [{'id': m['id'], 'value': m['value']} for m in metadata]
    for f in list(metadata_fields):
        if f['id'] in ['createdBy']:
            metadata_fields.remove(f)
    params = {
        'metadata': [{
            'flavor': 'dublincore/series',
            'fields': metadata_fields
        }],
        'acl': acl,
    }
    if theme:
        params['theme'] = theme
    files = [(k, (None, dumps(v).encode('utf-8'))) for k, v in params.items()]
    response = opencast_admin_client.post(url, files=files)
    response.raise_for_status()
    return response.json()


def get_events(opencast_admin_client, events_filter=None, events_sort='start_date:DESC', **kwargs):
    url = '/api/events'
    offset = 0
    batch_size = 20
    while offset >= 0:
        params = {
            'limit': batch_size,
            'offset': offset,
        }
        if events_filter:
            params['filter'] = events_filter
        if events_sort:
            params['sort'] = events_sort
        if kwargs:
            params |= kwargs
        response = opencast_admin_client.get(url, params=params)
        response.raise_for_status()
        for event_item in response.json():
            yield event_item
        if response.json():
            offset += batch_size
        else:
            offset = -1


def get_event_media(opencast_admin_client, mediapackage_id):
    url = f'/api/events/{mediapackage_id}/media'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()


def create_event(source_opencast_admin_client, source_opencast_presentation_client,
                 target_opencast_admin_client,
                 event_metadata, event_acl,
                 event_scheduling=None, event_processing=None,
                 presenter_track_url=None, presentation_track_url=None, audio_track_url=None):
    if not event_metadata or not event_acl:
        raise ValueError('Event metadata and acl are required but (partially) not set.')
    if not event_scheduling and not presenter_track_url and not presentation_track_url and not audio_track_url:
        raise ValueError('At least event scheduling information or presenter, presentation or audio track must be set.')
    url = f'/api/events/'
    params = [
        ('acl', (None, dumps(event_acl).encode('utf-8'))),
        ('metadata', (None, dumps(event_metadata).encode('utf-8'))),
    ]
    if event_scheduling:
        params.append(('scheduling', (None, dumps(event_scheduling).encode('utf-8'))))
    if event_processing:
        params.append(('processing', (None, dumps(event_processing).encode('utf-8'))))
    if presenter_track_url:
        track_file_name = filename_from_url(presenter_track_url)
        track_file_path = download_file(source_opencast_admin_client, source_opencast_presentation_client, presenter_track_url,
                                        event_metadata['identifier'], f'api_{track_file_name}')
        params.append(('presenter', (track_file_name, open(track_file_path))))
    if presentation_track_url:
        track_file_name = filename_from_url(presentation_track_url)
        track_file_path = download_file(source_opencast_admin_client, source_opencast_presentation_client, presentation_track_url,
                                        event_metadata['identifier'], f'api_{track_file_name}')
        params.append(('presentation', (track_file_name, open(track_file_path))))
    if audio_track_url:
        track_file_name = filename_from_url(audio_track_url)
        track_file_path = download_file(source_opencast_admin_client, source_opencast_presentation_client, audio_track_url,
                                        event_metadata['identifier'], f'api_{track_file_name}')
        params.append(('audio', (track_file_name, open(track_file_path))))
    result = target_opencast_admin_client.post(url, files=params)
    remove_mediapackage_tmp_dir(event_metadata['identifier'])
    result.raise_for_status()
    return result.json()


def get_event_acl(opencast_admin_client, mediapackage_id):
    url = f'/api/events/{mediapackage_id}/acl'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()


def update_event_acl(opencast_admin_client, mediapackage_id, acl):
    url = f'/api/events/{mediapackage_id}/acl'
    params = [
        ('acl', (None, dumps(acl).encode('utf-8')))
    ]
    response = opencast_admin_client.put(url, files=params)
    response.raise_for_status()
