#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from json import dumps, load
from os.path import join, abspath, isfile
from traceback import print_exc
from typing import Optional

from httpx import HTTPStatusError

import opencast
from opencast import externalapi, scheduler, assetmanager, search
from opencast.adminng import create_theme
from opencast.captureadmin import get_agents, update_agent_status, set_agent_capabilities
from opencast.client import OpencastClient
from opencast.externalapi import get_events, get_event_media
from opencast.ingest import schedule_mediapackage, ingest_zipped_mediapackage
from opencast.scheduler import update_schedule_with_technical_data
from opencast.series import get_series, get_series_acl, get_series_properties, update_series, update_series_property


def store_theme_id_mappings(source_opencast_client: OpencastClient, theme_id_mappings, tmp_dir='.'):
    if not theme_id_mappings:
        return
    filename = 'theme_id_mappings_' + source_opencast_client.base_url.host + '.json'
    filepath = join(abspath(tmp_dir), filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(dumps(theme_id_mappings))


def load_theme_id_mappings(source_opencast_client: OpencastClient, tmp_dir='.'):
    filename = 'theme_id_mappings_' + source_opencast_client.base_url.host + '.json'
    filepath = join(abspath(tmp_dir), filename)
    if isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return load(f)
    else:
        return dict()


def migrate_capture_agent(
        target_opencast_admin_client: OpencastClient,
        capture_agent_definition: dict):
    print(f'Create or update capture agent \"{capture_agent_definition["name"]}\".')
    update_agent_status(
        opencast_admin_client=target_opencast_admin_client,
        agent_name=capture_agent_definition.get('name'),
        agent_url=capture_agent_definition.get('url'))  # use default agent state
    set_agent_capabilities(
        opencast_admin_client=target_opencast_admin_client,
        agent_name=capture_agent_definition.get('name'),
        agent_capabilities=capture_agent_definition.get('capabilities'))


def migrate_theme(
        source_opencast_admin_client: OpencastClient,
        source_opencast_presentation_client: OpencastClient,
        target_opencast_admin_client: OpencastClient,
        target_opencast_presentation_client: OpencastClient,
        theme_id: str,
        tmp_dir: str):
    theme_id_mappings = load_theme_id_mappings(source_opencast_admin_client)
    # if theme is migrated before
    if theme_id in theme_id_mappings:
        # return target theme id
        return theme_id_mappings[theme_id]

    # otherwise migrate theme
    target_theme = create_theme(target_opencast_admin_client=target_opencast_admin_client,
                                target_opencast_presentation_client=target_opencast_presentation_client,
                                source_opencast_admin_client=source_opencast_admin_client,
                                source_opencast_presentation_client=source_opencast_presentation_client,
                                theme_id=theme_id, tmp_dir=tmp_dir)
    target_theme_id = str(target_theme['id'])
    theme_id_mappings[theme_id] = target_theme_id
    store_theme_id_mappings(source_opencast_admin_client, theme_id_mappings)
    return target_theme_id


def migrate_series(
        source_opencast_admin_client: OpencastClient,
        source_opencast_presentation_client: OpencastClient,
        target_opencast_admin_client: OpencastClient,
        target_opencast_presentation_client: OpencastClient,
        series_id: str,
        tmp_dir: str):
    try:
        target_series = externalapi.get_specific_series(
            opencast_admin_client=target_opencast_admin_client,
            series_id=series_id)
        if target_series:
            print(f'Series \'{target_series.get("title", "UNNAMED SERIES")}\' (ID: {series_id}) '
                  f'already exists on target system, skip migrating.')
            return
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            # series not found on target system, that is a common case
            pass
    series_dc = get_series(opencast_admin_client=source_opencast_admin_client, series_id=series_id)
    series_acl = get_series_acl(opencast_admin_client=source_opencast_admin_client, series_id=series_id)
    series_properties = get_series_properties(opencast_admin_client=source_opencast_admin_client, series_id=series_id)
    # TODO: handle series elements
    if not series_dc:
        print(f'ERROR: Unable to load series dublincore catalog for series with ID {series_id}.')
        raise ValueError(f'Series dublincore catalog is empty for series with ID: {series_id}.')
    update_series(opencast_admin_client=target_opencast_admin_client, series_xml=series_dc, acl_xml=series_acl)
    if series_properties:
        # set series properties
        for series_property in series_properties:
            for k, v in series_property.items():
                if 'theme' == k:
                    # fix theme ID
                    target_theme_id = migrate_theme(
                        source_opencast_admin_client=source_opencast_admin_client,
                        source_opencast_presentation_client=source_opencast_presentation_client,
                        target_opencast_admin_client=target_opencast_admin_client,
                        target_opencast_presentation_client=target_opencast_presentation_client,
                        theme_id=v,
                        tmp_dir=tmp_dir)
                    v = target_theme_id
                update_series_property(
                    opencast_admin_client=target_opencast_admin_client,
                    series_id=series_id,
                    property_name=k,
                    property_value=v)


def migrate_scheduled_episode(
        source_opencast_admin_client: OpencastClient,
        source_opencast_presentation_client: OpencastClient,
        target_opencast_admin_client: OpencastClient,
        source_event: dict,
        tmp_dir: str):
    target_event = None
    for event in get_events(
            opencast_admin_client=target_opencast_admin_client,
            events_filter=f'identifier:{source_event["identifier"]}'):
        target_event = event
        break
    if target_event:
        assert source_event['identifier'] == target_event['identifier']
        print(f'Episode \'{source_event["title"]}\' (ID: {source_event["identifier"]}) '
              f'already exists on target system, skip processing.')
        return None
    print(f'Migrate scheduled episode \'{source_event["title"]}\' (ID: {source_event["identifier"]})')
    source_mediapackage = scheduler.get_mediapackage(
        opencast_admin_client=source_opencast_admin_client,
        mediapackage_id=source_event['identifier'])
    source_schedule = scheduler.get_schedule_technical(
        opencast_admin_client=source_opencast_admin_client,
        mediapackage_id=source_event['identifier'])
    if not 'agentConfig' in source_schedule:
        raise ValueError(f'Schedule metadata invallid for episode '
                         f'\'{source_event["title"]}\' (ID: {source_event["identifier"]})')
    workflow_definition_id = source_schedule.get('agentConfig').get('org.opencastproject.workflow.definition', '')
    schedule_mediapackage(
        source_opencast_admin_client=source_opencast_admin_client,
        source_opencast_presentation_client=source_opencast_presentation_client,
        target_opencast_admin_client=target_opencast_admin_client,
        mediapackage=source_mediapackage,
        workflow_definition_id=workflow_definition_id,
        workflow_properties=source_schedule.get('agentConfig'),
        tmp_dir=tmp_dir)
    # technical scheduling dates may differ from metadata catalog.
    update_schedule_with_technical_data(
        opencast_admin_client=target_opencast_admin_client,
        mediapackage_id=source_event["identifier"],
        start=source_schedule['start'],
        end=source_schedule['end'],
        agent=source_schedule['location'])
    print(f'Migration of scheduled episode \'{source_event["title"]}\' (ID: {source_event["identifier"]}) done.')


def migrate_archived_episode(
        source_opencast_admin_client: OpencastClient,
        source_opencast_presentation_client: OpencastClient,
        target_opencast_admin_client: OpencastClient,
        source_event: dict,
        workflow_definition_id: str,
        workflow_properties: dict,
        tmp_dir: str):
    target_event = None
    for event in get_events(
            opencast_admin_client=target_opencast_admin_client,
            events_filter=f'identifier:{source_event["identifier"]}'):
        target_event = event
        break
    if target_event:
        assert source_event['identifier'] == target_event['identifier']
        print(f'Episode \'{source_event["title"]}\' (ID: {source_event["identifier"]}) '
              f'already exists on target system, skip processing.')
        return None
    print(f'Migrate episode \'{source_event["title"]}\' (ID: {source_event["identifier"]})')
    source_mediapackage = assetmanager.get_mediapackage(
        opencast_admin_client=source_opencast_admin_client,
        mediapackage_id=source_event['identifier'])
    if source_event['publication_status'] and 'engage-player' in source_event['publication_status']:
        search_mediapackage = search.get_mediapackage(
            opencast_presentation_client=source_opencast_presentation_client,
            mediapackage_id=source_event["identifier"])
        if not search_mediapackage:
            print(f'ERROR: Search publication not exists for episode '
                  f'\'{source_event["title"]}\' (ID: {source_event["identifier"]}). Skip processing search publication.')
        else:
            search_mediapackage.remove_publication()

            def migrate_search_element_filter(element):
                return not element.tag.endswith('track') or \
                       (element.tag.endswith('track') and 'transport' not in element.keys())

            tags = ['+search']
            if 'api' in source_event['publication_status']:
                tags.append('+externalapi')
            search_mediapackage.apply_tags(tags=tags, element_filter=migrate_search_element_filter)
            source_mediapackage.merge(other=search_mediapackage, element_filter=migrate_search_element_filter)
    if source_event['publication_status'] and 'internal' in source_event['publication_status']:
        try:
            source_mediapackage.add_elements_from_publication(
                publication_channel='internal', tags=['+internal'])
        except:
            print_exc()
            print(f'ERROR: Failed to parse editor data for episode '
                  f'\'{source_event["title"]}\' (ID: {source_event["identifier"]}). Skip editor preview.')
    try:
        event_workflow_properties = assetmanager.get_workflow_properties(
            opencast_admin_client=source_opencast_admin_client,
            mediapackage_id=source_mediapackage.get_identifier())
    except:
        event_workflow_properties = dict()
    source_mediapackage.remove_publication()
    workflow_instance_xml = ingest_zipped_mediapackage(
        source_opencast_admin_client=source_opencast_admin_client,
        source_opencast_presentation_client=source_opencast_presentation_client,
        target_opencast_admin_client=target_opencast_admin_client,
        mediapackage=source_mediapackage,
        workflow_definition_id=workflow_definition_id,
        workflow_properties={**workflow_properties, **event_workflow_properties},
        tmp_dir=tmp_dir)
    print(f'Migration of episode \'{source_event["title"]}\' (ID: {source_event["identifier"]}) done.')
    return workflow_instance_xml


def migrate_data(
        source_opencast_admin_client: OpencastClient,
        source_opencast_presentation_client: OpencastClient,
        target_opencast_admin_client: OpencastClient,
        target_opencast_presentation_client: OpencastClient,
        workflow_definition_id: str,
        workflow_properties: dict,
        series_id: Optional[str],
        tmp_dir: str):

    # migrate capture agents
    for agent in get_agents(source_opencast_admin_client):
        try:
            migrate_capture_agent(
                target_opencast_admin_client=target_opencast_admin_client,
                capture_agent_definition=agent)
        except:
            print_exc()
            print(f'ERROR: Unable to migrate capture agent \'{agent["name"]}\'.')

    # migrate series
    for series in externalapi.get_series(
            opencast_admin_client=source_opencast_admin_client,
            series_filter=f'identifier:{series_id}' if series_id else None):
        print(f'Migrate series \'{series.get("title", "UNNAMED SERIES")}\' (ID: {series.get("identifier", "-")}).')
        migrate_series(
            source_opencast_admin_client=source_opencast_admin_client,
            source_opencast_presentation_client=source_opencast_presentation_client,
            target_opencast_admin_client=target_opencast_admin_client,
            target_opencast_presentation_client=target_opencast_presentation_client,
            series_id=series['identifier'],
            tmp_dir=tmp_dir)

    # migrate episodes
    for source_event in get_events(
            opencast_admin_client=source_opencast_admin_client,
            events_filter=f'series:{series_id}' if series_id else None):
        if source_event.get('status', None) == 'EVENTS.EVENTS.STATUS.RECORDING':
            print(f'Skip migrating recording episode \'{source_event.get("title", "UNNAMED EPISODE")}\' '
                  f'(ID: {source_event.get("identifier", "-")}).')
            continue
        is_scheduled_event = False
        try:
            if source_event.get('processing_state', '') == '':
                if source_event.get('status', None) == 'EVENTS.EVENTS.STATUS.SCHEDULED':
                    # this event may be scheduled
                    # double check event does not contain any media files
                    source_event_media = get_event_media(
                        opencast_admin_client=source_opencast_admin_client,
                        mediapackage_id=source_event['identifier'])
                    if len(source_event_media) == 0:
                        is_scheduled_event = True
            elif source_event.get('processing_state', '') != 'SUCCEEDED':
                print(
                    f'Processing state of episode \'{source_event["title"]}\' (ID: {source_event["identifier"]}) is '
                    f'\'{source_event.get("processing_state", "UNKNOWN")}\', skip Processing')
                continue
            if is_scheduled_event:
                migrate_scheduled_episode(
                    source_opencast_admin_client=source_opencast_admin_client,
                    source_opencast_presentation_client=source_opencast_presentation_client,
                    target_opencast_admin_client=target_opencast_admin_client,
                    source_event=source_event,
                    tmp_dir=tmp_dir)
            else:
                workflow_instance_xml = migrate_archived_episode(
                    source_opencast_admin_client=source_opencast_admin_client,
                    source_opencast_presentation_client=source_opencast_presentation_client,
                    target_opencast_admin_client=target_opencast_admin_client,
                    source_event=source_event,
                    workflow_definition_id=workflow_definition_id,
                    workflow_properties=workflow_properties,
                    tmp_dir=tmp_dir)
                if workflow_instance_xml is not None:
                    assert source_event['identifier'] in workflow_instance_xml
        except KeyboardInterrupt:
            exit(0)
        except Exception:
            print_exc()
            print(
                f'ERROR: Unable to migrate episode \'{source_event["title"]}\' (ID: {source_event["identifier"]}).')


def main():
    tmp_dir = opencast.tmp_dir
    source_opencast_admin_url = 'https://stable.opencast.org'
    source_opencast_presentation_url = 'https://stable.opencast.org'
    source_opencast_username = 'admin'
    source_opencast_password = 'opencast'
    source_auth = (source_opencast_username, source_opencast_password)

    target_opencast_admin_url = 'http://localhost:8080'
    target_opencast_presentation_url = 'http://localhost:8080'
    target_opencast_username = 'admin'
    target_opencast_password = 'opencast'
    target_auth = (target_opencast_username, target_opencast_password)

    workflow_definition_id = 'import'
    workflow_properties = {}

    series_id = None
    default_timeout = 300

    with OpencastClient(source_opencast_admin_url,
                        auth=source_auth,
                        timeout=default_timeout) as source_opencast_admin_client:
        with OpencastClient(source_opencast_presentation_url,
                            auth=source_auth,
                            timeout=default_timeout) as source_opencast_presentation_client:
            with OpencastClient(target_opencast_admin_url,
                                auth=target_auth,
                                timeout=default_timeout) as target_opencast_admin_client:
                with OpencastClient(target_opencast_presentation_url,
                                    auth=target_auth,
                                    timeout=default_timeout) as target_opencast_presentation_client:
                    print('Start data migration.')
                    try:
                        migrate_data(
                            source_opencast_admin_client=source_opencast_admin_client,
                            source_opencast_presentation_client=source_opencast_presentation_client,
                            target_opencast_admin_client=target_opencast_admin_client,
                            target_opencast_presentation_client=target_opencast_presentation_client,
                            workflow_definition_id=workflow_definition_id,
                            workflow_properties=workflow_properties,
                            series_id=series_id,
                            tmp_dir=tmp_dir)
                        print('Data migration was successful.')
                    except KeyboardInterrupt:
                        exit(0)


if __name__ == '__main__':
    main()
