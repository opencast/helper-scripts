#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

import config
from data_handling.elements import get_id
from data_handling.errors import MediaPackageError
from data_handling.parse_manifest import parse_manifest_from_endpoint
from import_mp.import_mp import import_mp
from input_output.input import get_yes_no_answer
from rest_requests.api_requests import get_events_of_series
from rest_requests.assetmanager_requests import get_media_package
from rest_requests.request_error import RequestError
from parse_args import parse_args
from args.digest_login import DigestLogin


def main():
    """
    Ingest the given events into another tenant of the same OC system
    """

    event_ids, series_ids = parse_args()
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)

    # get events from all series
    if series_ids:
        print("Getting events for series")
        events = []
        for series_id in series_ids:
            try:
                events_of_series = get_events_of_series(config.source_url, digest_login, series_id)
                events += events_of_series
            except RequestError as e:
                print("Events of series {} could not be requested: {}".format(series_id, e.error))
            except Exception as e:
                print("Events of series {} could not be requested: {}".format(series_id, str(e)))

        if not events:
            __abort_script("No events found.")

        # check if this is correct
        print("The following events will be imported:")
        for event in events:
            print("%36s | %s" % (event["identifier"], event["title"]))
        print()

        start_process = get_yes_no_answer("Continue?")

        if not start_process:
            __abort_script("Okay, not importing anything.")

        event_ids = [get_id(event) for event in events]

    print("Starting import process.")
    for event_id in event_ids:
        try:
            mp = get_media_package(config.source_url, digest_login, event_id)

            series_id, tracks, catalogs, attachments = parse_manifest_from_endpoint(mp, event_id, False)

            workflow = import_mp(series_id, tracks, catalogs, attachments, config.target_url, digest_login,
                                 config.workflow_id, config.workflow_config, False, True)

            print("Imported media package {} (new id: {}) and started workflow {} with id {}.".
                  format(event_id, workflow.mp_id, workflow.template, workflow.id))

        except MediaPackageError as e:
            print("Event {} could not be imported: {}".format(event_id, str(e)))
        except RequestError as e:
            print("Event {} could not be imported: {}".format(event_id, e.error))
        except Exception as e:
            print("Event {} could not be imported: {}".format(event_id, str(e)))

    print("Done.")


def __abort_script(message):
    print(message)
    sys.exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
