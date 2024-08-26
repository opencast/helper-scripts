#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from opencast.mediapackage import Mediapackage


def get_mediapackage(opencast_admin_client, mediapackage_id):
    url = f'/recordings/{mediapackage_id}/mediapackage.xml'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return Mediapackage(response.text.encode('utf-8'))


def get_schedule_technical(opencast_admin_client, mediapackage_id):

    url = f'/recordings/{mediapackage_id}/technical.json'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()


def update_schedule_with_technical_data(opencast_admin_client, mediapackage_id, mediapackage_xml=None,
                                        start=None, end=None, agent=None, users=None,
                                        workflow_properties=None, agent_properties=None):
    """
    Update an schedule in opencast with the given data.

    Parameters
    ----------
    opencast_admin_client: OpencastClient
        Opencast client
    mediapackage_id: str
        Episode identifier
    mediapackage_xml: str, optional
        Optional argument. The mediapackage to update
    start: str, optional
        Optional argument. The schedule start date time in UTC as RFC string.
    end: str, optional
        Optional argument. The schedule end date time in UTC as RFC string.
    agent: str, optional
        Optional argument. The capture agent identifier.
    users: list, optional
        Optional argument. List of user identifier (speakers/lecturers) for the episode to update.
    workflow_properties: dict, optional
        Optional argument. Workflow properties.
    agent_properties: dict, optional
        Optional argument. Capture agent properties.
    """
    url = f'/recordings/{mediapackage_id}/'
    params = dict()
    if start:
        params['start'] = int(datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z').timestamp()*1000)
    if end:
        params['end'] = int(datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z').timestamp()*1000)
    if agent:
        params['agent'] = agent
    if users:
        params['users'] = ','.join(users)
    if mediapackage_xml:
        params['mediaPackage'] = mediapackage_xml
    if workflow_properties:
        params['wfproperties'] = '\n'.join([f'{k}={v}' for k, v in workflow_properties.items()])
    if agent_properties:
        params['agentparameters'] = '\n'.join([f'{k}={v}' for k, v in agent_properties.items()])
    if not params:
        raise ValueError('At least one of the optional parameters to update schedule must be set.')
    print(f'Update schedule for media package {mediapackage_id}.')
    response = opencast_admin_client.put(url, params=params)
    response.raise_for_status()
