#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from traceback import print_exc

from opencast.client import OpencastClient
from opencast.externalapi import (get_event_media, get_events)


def check_publications_exists(source_opencast_admin_client, target_opencast_admin_client):
    """
    Go through all archived episodes on source Opencast system and
    check existence of publications on the target Opencast system.
    If a publication X exists in source system but not on the target, we will print a log message to stdout.
    """
    for source_event in get_events(source_opencast_admin_client):
        try:
            if source_event.get('processing_state', '') == '':
                if source_event.get('status', None) == 'EVENTS.EVENTS.STATUS.SCHEDULED':
                    # this event may be scheduled
                    # double check event does not contain any media files
                    source_event_media = get_event_media(source_opencast_admin_client, source_event['identifier'])
                    if len(source_event_media) == 0:
                        continue
            elif source_event.get('processing_state', '') != 'SUCCEEDED':
                print(f'Processing state of episode \'{source_event["title"]}\' (ID: {source_event["identifier"]}) is '
                      f'\'{source_event.get("processing_state", "UNKNOWN")}\', skip Processing')
                continue

            source_publications = source_event.get('publication_status', [])
            if not source_publications:
                continue
            events_found = 0
            for target_event in get_events(target_opencast_admin_client, events_filter=f'identifier:{source_event["identifier"]}'):
                assert(source_event['identifier'] == target_event['identifier'])
                events_found += 1
                target_publications = target_event.get('publication_status', [])
                for publication in source_publications:
                    if publication not in target_publications:
                        print(f'Event \'{source_event["title"]}\' (ID: {source_event["identifier"]}) '
                              f'lack of {publication} publication on target system.')
            if events_found == 0:
                print(f'Event \'{source_event["title"]}\' (ID: {source_event["identifier"]}) '
                      f'does not exist on target system.')
        except KeyboardInterrupt:
            exit(0)
        except:
            print_exc()
            print(f'ERROR: Unable to check episode \'{source_event["title"]}\' (ID: {source_event["identifier"]}) publications.')


def main():
    source_opencast_admin_url = 'https://stable.opencast.org'
    source_opencast_username = 'admin'
    source_opencast_password = 'opencast'
    source_auth = (source_opencast_username, source_opencast_password)

    target_opencast_admin_url = 'http://localhost:8080'
    target_opencast_username = 'admin'
    target_opencast_password = 'opencast'
    target_auth = (target_opencast_username, target_opencast_password)

    with OpencastClient(source_opencast_admin_url, auth=source_auth) as source_opencast_admin_client:
        with OpencastClient(target_opencast_admin_url, auth=target_auth) as target_opencast_admin_client:
            print('Start checking publications.')
            check_publications_exists(source_opencast_admin_client, target_opencast_admin_client)
            print('Done.')


if __name__ == '__main__':
    main()
