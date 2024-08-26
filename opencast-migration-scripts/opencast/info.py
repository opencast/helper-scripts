#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_me_json(opencast_client, **kwargs):
    url = '/info/me.json'
    response = opencast_client.get(url, **kwargs)
    response.raise_for_status()
    return response.json()


def get_version(opencast_client, **kwargs):
    url = '/sysinfo/bundles/version'
    params = {
        'prefix': 'opencast'
    }
    response = opencast_client.get(url, **kwargs)
    response.raise_for_status()
    return response.json()
