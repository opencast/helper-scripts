#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opencast.mediapackage import Mediapackage, PublicationMediapackageElement


def get_mediapackage(opencast_admin_client, mediapackage_id):
    url = f'/assets/episode/{mediapackage_id}'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return Mediapackage(response.text.encode('utf-8'))


def get_workflow_properties(opencast_admin_client, mediapackage_id):
    url = f'/assets/{mediapackage_id}/workflowProperties.json'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()
