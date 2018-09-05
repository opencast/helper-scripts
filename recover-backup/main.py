#!/usr/bin/env python3

""" This module contains the main method. """

import sys

from script.check_mediapackages import check_recovery_start
from script.get_mediapackages import get_mediapackages, get_all_mediapackages
from script.parse_args import parse_args
from script.recover_mediapackage import recover_mp
from util.base_url import get_base_url, DEFAULT_TENANT
from script.get_mediapackage_elements import MediapackageError
from util.request_error import RequestError


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
        mps_to_recover = get_all_mediapackages(backup, tenant, lastversion)

    else:
        mps_to_recover = get_mediapackages(mediapackages, backup, tenant, lastversion)

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

        print("Finished.")


if __name__ == '__main__':
    main()
