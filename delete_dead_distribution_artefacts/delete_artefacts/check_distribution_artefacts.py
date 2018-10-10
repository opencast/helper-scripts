"""
This module checks which distribution artefacts belong to mediapackages that no longer exist.
"""
from collections import defaultdict
from rest_requests.assetmanager_requests import media_package_exists
from rest_requests.request_error import RequestError


def check_distribution_artefacts(distribution_artefacts, url_builder, digest_login, progress_printer):
    """
    Check distribution artefacts for whether their media packages still exist.

    :param distribution_artefacts: The distribution artefacts to be checked.
    :type distribution_artefacts: dict
    :param url_builder: Object to build the URL for requests
    :type url_builder: URLBuilder
    :param digest_login: The login data_handling for digest authentication
    :type digest_login: DigestLogin
    :param progress_printer: Object to print progress bars.
    :type progress_printer: ProgressPrinter
    :return: The distribution artefacts for which the media package no longer exists.
    :rtype: dict
    """

    total = sum([len(distribution_artefacts[tenant].keys()) for tenant in distribution_artefacts.keys()])
    count = 0

    progress_printer.print_message("Checking {} media packages... ".format(total), 0)

    dead_distribution_artefacts = defaultdict(lambda: defaultdict(lambda: list))

    for tenant in distribution_artefacts.keys():

        base_url = url_builder.get_base_url(tenant)

        for media_package in distribution_artefacts[tenant].keys():

            try:
                if not media_package_exists(base_url, digest_login, media_package):
                    dead_distribution_artefacts[tenant][media_package] = distribution_artefacts[tenant][media_package]
            except RequestError as e:
                print("Media package {} could not be checked: {}".format(media_package, e.error))

            progress_printer.print_progress(count, total)
            count += 1

    return dead_distribution_artefacts
