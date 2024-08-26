#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_all_series(opencast_admin_client, sort='CREATED_DESC', **kwargs):
    url = f'/series/series.json'
    limit = 10
    page = 0
    params = {
        'count': limit,
        'sort': sort
    }
    for (k, v) in kwargs.items():
        params[k] = v
    while page >= 0:
        params['startPage'] = page
        response = opencast_admin_client.get(url, params=params)
        response.raise_for_status()
        series_json = response.json()
        if int(series_json.get('totalCount', -1)) > 0:
            for catalog in series_json.get('catalogs', []):
                for catalog_type, values in catalog.items():
                    if catalog_type != 'http://purl.org/dc/terms/':
                        continue
                    series = {}
                    for vname, vlist in values.items():
                        series[vname] = vlist[0]['value']
                    yield series
            if series_json.get('catalogs', []):
                page += 1
            else:
                page = -1
        else:
            page = -1


def get_series(opencast_admin_client, series_id):
    url = f'/series/{series_id}.xml'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.text


def get_series_acl(opencast_admin_client, series_id):
    url = f'/series/{series_id}/acl.xml'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.text


def get_series_elements(opencast_admin_client, series_id):
    url = f'/series/{series_id}/elements.json'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()


def get_series_element(opencast_admin_client, series_id, element_type):
    url = f'/series/{series_id}/elements/{element_type}'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.text


def get_series_properties(opencast_admin_client, series_id):
    url = f'/series/{series_id}/properties.json'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()


def update_series(opencast_admin_client, series_xml, acl_xml):
    url = '/series/'
    params = {
        'series': series_xml,
        'acl': acl_xml,
    }
    response = opencast_admin_client.post(url, data=params)
    response.raise_for_status()
    return response.text


def update_series_property(opencast_admin_client, series_id, property_name, property_value):
    url = f'/series/{series_id}/property'
    params = {
        'name': property_name,
        'value': property_value
    }
    response = opencast_admin_client.post(url, data=params)
    response.raise_for_status()
