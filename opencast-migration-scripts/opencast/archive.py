#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from opencast.mediapackage import Mediapackage


def get_all_episodes(opencast_admin_client, sort='DATE_CREATED_DESC', **kwargs):
    url = f'/archive/episode.json'
    limit = 10
    offset = 0
    params = {
        'limit': limit,
        'sort': sort,
        'onlyLatest': True,
        'admin': True,
        'episodes': False,
    }
    for (k, v) in kwargs.items():
        params[k] = v
    while offset >= 0:
        params['offset'] = offset
        response = opencast_admin_client.get(url, params=params)
        response.raise_for_status()
        if 'search-results' not in response.json():
            offset = -1
        else:
            for episode in response.json().get('search-results').get('result', []):
                yield episode
            if response.json().get('search-results').get('result', []):
                offset += limit
            else:
                offset = -1


def get_mediapackage(opencast_admin_client, episode_id):
    url = f'/archive/archive/mediapackage/{episode_id}'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return Mediapackage(response.text.encode('utf-8'))
