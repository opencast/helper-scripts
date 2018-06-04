#!/usr/bin/env python3

""" This module contains the main method. """

import sys

from script.input.check_recovery_start import check_recovery_start
from script.find_mediapackages import find_mediapackages, find_all_mediapackages
from script.input.parse_args import parse_args
from script.recover import recover_mp
from script.input.base_url import get_base_url, DEFAULT_TENANT
from script.parsing.parse_manifest import MediapackageError
from script.requests.util.request_error import RequestError


def main():
    """
    Parse the arguments, get mediapackages for recovery and check these for correctness before attempting to recover
    them.
    """

    # parse arguments
    opencast, https, digest_login, backup, mediapackages, tenant, workflow_id, lastversion = parse_args()

    if not tenant:
        print("No tenant provided, using default tenant.")
        tenant = DEFAULT_TENANT
    if lastversion:
        print("Always using last version of mediapackages.")

    base_url = get_base_url(opencast, https, tenant)

    # get paths to mediapackages to be recovered
    if not mediapackages:
        print("No mediapackages provided"
              ", recovering all.")
        mps_to_recover = find_all_mediapackages(backup, tenant, lastversion)

    else:
        mps_to_recover = find_mediapackages(mediapackages, backup, tenant, lastversion)

    if not mps_to_recover:
        # abort recovery
        print("There are no mediapackages that can be recovered.")
        sys.exit()

    # check if these should be recovered
    start_recovery = check_recovery_start(mps_to_recover)

    if not start_recovery:
        # abort recovery
        print("Okay, not recovering anything.")
        sys.exit()

    else:
        # start recovery
        print("Starting recovery process.")

        for mp in mps_to_recover:

            try:
                workflow = recover_mp(mp, base_url, digest_login, workflow_id)
                print("Recovered mediapackage {} (new id: {}) and started workflow {} with id {}.".
                      format(mp.id, workflow.mp_id, workflow.template, workflow.id))
            except MediapackageError as e:
                print("Mediapackage {} could not be recovered: {}".format(mp.id, str(e)))
            except RequestError as e:
                print("Mediapackage {} could not be recovered: {}".format(mp.id, e.error))
            except Exception as e:
                print("Mediapackage {} could not be recovered: {}".format(mp.id, str(e)))

        print("Finished.")


if __name__ == '__main__':
    main()
