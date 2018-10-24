#!/usr/bin/env python3

"""
This script deletes distribution artefacts of media packages that no longer exist.
"""
import sys
import os

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

from delete_artefacts.check_distribution_artefacts import check_distribution_artefacts
from delete_artefacts.delete_dead_distribution_artefacts import \
    delete_dead_distribution_artefacts
from delete_artefacts.find_distribution_artefacts import find_distribution_artefacts
from input.present_dead_distribution_artefacts import present_dead_distribution_artefacts, PresentAnswer
from input.parse_args import parse_args
from args.url_builder import URLBuilder
from input_output.log_writer import LogWriter
from rest_requests.tenant_requests import filter_tenants
from input_output.progress_printer import ProgressPrinter
from rest_requests.request_error import RequestError


def main():
    """
    Parse the arguments, find the distribution artefacts and delete those for which the media package no longer exist.
    """

    # parse args
    opencast, distribution_dirs, https, chosen_tenants, excluded_tenants, channels, digest_login, silent, \
    no_fancy_output = parse_args()

    print()

    url_builder = URLBuilder(opencast, https)
    progress_printer = ProgressPrinter(silent, no_fancy_output)
    tenants = filter_tenants(chosen_tenants, excluded_tenants, progress_printer, url_builder, digest_login)

    if not tenants:
        progress_printer.print_if_silent("No tenants remain.")
        sys.exit()

    if not channels:
        print("No channels defined, considering all channels.")

    # find distribution artefacts
    distribution_artefacts = find_distribution_artefacts(distribution_dirs, tenants, channels, progress_printer)

    if not distribution_artefacts:
        progress_printer.print_if_silent("No distribution artefacts found.")
        sys.exit()

    # find out which distribution artefacts belong to media packages that no longer exist
    dead_distribution_artefacts = check_distribution_artefacts(distribution_artefacts, url_builder, digest_login,
                                                               progress_printer)
    if not dead_distribution_artefacts:
        progress_printer.print_if_silent("No distribution artefacts for deleted media packages found.")
        sys.exit()

    # check whether the dead distribution artefacts should be deleted
    present_answer = present_dead_distribution_artefacts(dead_distribution_artefacts)

    if present_answer == PresentAnswer.QUIT:
        sys.exit()

    # start recovery
    log_writer = LogWriter("deleted_distribution_artefacts_log", 'tenant', 'media package', 'distribution artefact')
    delete_dead_distribution_artefacts(dead_distribution_artefacts, log_writer, progress_printer, present_answer)

    log_writer.close_log()
    progress_printer.print_if_silent("Deletion finished.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting script.")
        sys.exit(0)
    except RequestError as e:
        print("Distribution artefacts could not be deleted: {}".format(e.error))
