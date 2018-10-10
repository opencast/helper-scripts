#!/usr/bin/env python3

"""
This script deletes distribution artefacts of mediapackages that no longer exist.
"""
import sys
import os

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

from delete_artefacts.check_distribution_artefacts import check_distribution_artefacts
from delete_artefacts.delete_dead_distribution_artefacts import \
    delete_dead_distribution_artefacts
from delete_artefacts.find_distribution_artefacts import find_distribution_artefacts
from input.check_deletion_start import check_deletion_start
from input.parse_args import parse_args
from args.url_builder import URLBuilder
from input_output.log_writer import LogWriter
from rest_requests.filter_tenants import filter_tenants
from utility.progress_printer import ProgressPrinter


def main():
    """
    Parse the arguments, find the distribution artefacts and delete those for which the media package no longer exist.
    """

    # parse args
    opencast, distribution_dirs, https, chosen_tenants, excluded_tenants, digest_login, silent, no_fancy_output\
        = parse_args()

    url_builder = URLBuilder(opencast, https)
    progress_printer = ProgressPrinter(silent, no_fancy_output)
    tenants = filter_tenants(chosen_tenants, excluded_tenants, progress_printer, url_builder, digest_login)
    log_writer = LogWriter("deleted_distribution_artefacts_log", 'tenant', 'media package', 'distribution artefact')

    # find distribution artefacts
    distribution_artefacts = find_distribution_artefacts(distribution_dirs, tenants, progress_printer)

    if not distribution_artefacts:
        # abort recovery
        sys.exit()

    # find out which distribution artefacts belong to mediapackages that no longer exist
    dead_distribution_artefacts = check_distribution_artefacts(distribution_artefacts, url_builder, digest_login,
                                                               progress_printer)

    if not dead_distribution_artefacts:
        # abort recovery
        print("There are no distribution artefacts that can be deleted.")
        sys.exit()

    # check whether the dead distribution artefacts should be deleted
    start_deletion = check_deletion_start(dead_distribution_artefacts)

    if not start_deletion:
        # abort recovery
        print("Okay, not deleting anything.")
        sys.exit()

    else:
        # start recovery
        delete_dead_distribution_artefacts(dead_distribution_artefacts, log_writer, progress_printer)

    log_writer.close_log()
    if silent:
        print("Deletion finished.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting script.")
        sys.exit(0)
