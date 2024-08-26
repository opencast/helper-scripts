#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml.etree import fromstring

from opencast.mediapackage import Mediapackage

namespaces = {
    "mp": "http://mediapackage.opencastproject.org",
    "ns2": "http://search.opencastproject.org",
    "ns3": "http://org.opencastproject.security",
}


def get_mediapackage(opencast_presentation_client, mediapackage_id):
    url = '/search/episode.xml'
    params = {'id': mediapackage_id}
    response = opencast_presentation_client.get(url, params=params)
    response.raise_for_status()
    search_result = response.text.encode('utf-8')
    search_result_element = fromstring(search_result)
    mediapackage_str = search_result_element.findtext('.//ns2:ocMediapackage', namespaces=namespaces)
    if mediapackage_str:
        return Mediapackage(mediapackage_str.encode('utf-8'))
    return None


def get_mediapackages(opencast_presentation_client, sort="MEDIA_PACKAGE_ID"):
    url = '/search/episode.xml'
    params = {
        'admin': True,
        'sort': sort
    }
    offset = 0
    batch_size = 10
    while offset >= 0:
        params['limit'] = batch_size
        params['offset'] = offset
        response = opencast_presentation_client.get(url, params=params)
        response.raise_for_status()
        itemsfound = 0
        search_results = fromstring(response.text.encode('utf-8'))
        for mediapackage in search_results.iterfind('.//ns2:ocMediapackage', namespaces=namespaces):
            itemsfound += 1
            yield Mediapackage(mediapackage.text.encode('utf-8'))
        if itemsfound > 0:
            offset += itemsfound
        else:
            offset = -1
