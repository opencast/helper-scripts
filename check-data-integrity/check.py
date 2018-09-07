#!/usr/bin/env python3

"""
This script checks if certain data in opencast is missing, out-of-date or otherwise malformed and reports the affected
series and events for each tenant.
"""

from args.check_settings import CheckSettings
from check_data.get_assets import get_asset_of_series, get_series_of_event, get_assets_of_event, get_assets_of_oaipmh
from check_data.malformed import Malformed
from check_data.types import AssetType
from data_handling.element_util import get_id, published_to_oaipmh
from rest_requests.oaipmh_requests import get_oaipmh_record, get_oaipmh_publications
from util.error_collector import ErrorCollector
from rest_requests.basic_requests import get_events, get_tenants, get_series
from args.parse_args import parse_args
from util.progress_printer import ProgressPrinter
from rest_requests.request_error import RequestError
from args.url_builder import URLBuilder


def check_assets_of_series(series, opencast_url, digest_login, asset_type, error_collector, progress_printer):
    """
    Get ACLs or dublincores of all series and put them in a dict. If some of them are malformed, collect their errors.

    :param series: all series
    :type series: list
    :param opencast_url:
    :type opencast_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :param asset_type:
    :type asset_type: AssetType
    :param error_collector:
    :type error_collector: ErrorCollector
    :param progress_printer:
    :type progress_printer: ProgressPrinter
    :return: Map with series ids and the associated assets
    :rtype: dict
    """

    series_asset_map = {}

    for count, a_series in enumerate(series):

        progress_printer.print_progress(count, len(series))

        series_asset = get_asset_of_series(a_series, opencast_url, digest_login, asset_type)

        if isinstance(series_asset, Malformed):
            error_collector.collect_errors(series_asset, get_id(a_series))

        series_asset_map[get_id(a_series)] = series_asset

    if len(series) != len(series_asset_map.keys()):
        raise ValueError("Less series {}s than series!".format(asset_type))

    return series_asset_map


def check_series_of_events(events, series, error_collector, progress_printer, no_series_error):
    """
    Get series for each event if it belongs to one. If some of them are malformed, collect their errors.

    :param events:
    :type events: list
    :param series:
    :type series: list
    :param error_collector:
    :type error_collector: ErrorCollector
    :param progress_printer:
    :type progress_printer: ProgressPrinter
    :param no_series_error: Whether events without series are wrong
    :type no_series_error: bool
    :return: Map with event id and the associated series or None
    :rtype: dict
    """

    event_series_map = {}

    for count, event in enumerate(events):

        progress_printer.print_progress(count, len(events))

        series_of_event = get_series_of_event(series, event, no_series_error)

        if isinstance(series_of_event, Malformed):
            error_collector.collect_errors(series_of_event, get_id(event))

        event_series_map[get_id(event)] = series_of_event

    return event_series_map


def check_assets_of_events(events, event_series_map, series_asset_map, opencast_url, digest_login, asset_type,
                           error_collector, progress_printer):
    """
    Get ACLs or dublincores of all events and put them in a dict. If some of them are malformed, collect their errors.

    :param events:
    :type events: list
    :param event_series_map:
    :type event_series_map: dict
    :param series_asset_map:
    :type series_asset_map: dict
    :param opencast_url:
    :type opencast_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :param asset_type:
    :type asset_type: AssetType
    :param error_collector:
    :type error_collector: ErrorCollector
    :param progress_printer:
    :type progress_printer: ProgressPrinter
    :return: Map with event ids and the associated assets
    :rtype: dict
    """

    event_asset_map = {}

    for count, event in enumerate(events):

        progress_printer.print_progress(count, len(events))

        series_of_event = event_series_map[get_id(event)]

        if series_of_event and not isinstance(series_of_event, Malformed):
            series_asset_of_series = series_asset_map[get_id(series_of_event)]
        else:
            series_asset_of_series = None

        episode_asset, series_asset = get_assets_of_event(event, opencast_url, digest_login, series_of_event,
                                                          series_asset_of_series, asset_type)

        if isinstance(episode_asset, Malformed):
            error_collector.collect_errors(episode_asset, get_id(event))
        if isinstance(series_asset, Malformed):
            error_collector.collect_errors(series_asset, get_id(event))

        event_asset_map[get_id(event)] = (episode_asset, series_asset)

    return event_asset_map


def check_oaipmh(oaipmh_events, event_series_map, event_dc_map, event_acl_map, digest_login, error_collector,
                 opencast_url, progress_printer):
    """
    Check OAIPMH by getting all ACLs and dublincore catalogs from each record and comparing them with those from the
    corresponding event. Collect any errors.

    (Currently doesn't return anything since this is the last check.)

    :param oaipmh_events: All events published to OAIPMH
    :type oaipmh_events: list
    :param event_series_map:
    :type event_series_map: dict
    :param event_dc_map:
    :type event_dc_map: dict
    :param event_acl_map:
    :type event_acl_map: dict
    :param digest_login:
    :type digest_login: DigestLogin
    :param error_collector:
    :type error_collector: ErrorCollector
    :param opencast_url:
    :type opencast_url: str
    :param progress_printer:
    :type progress_printer: ProgressPrinter
    """

    for count, event in enumerate(oaipmh_events):

        progress_printer.print_progress(count, len(oaipmh_events))

        series_of_event = event_series_map[get_id(event)]
        episode_dc, series_dc = event_dc_map[get_id(event)]
        episode_acl, series_acl = event_acl_map[get_id(event)]

        oaipmh_publications = get_oaipmh_publications(event)

        for oaipmh_repo, oaipmh_url in oaipmh_publications:

            # get oaipmh record
            try:
                oaipmh_record = get_oaipmh_record(event, oaipmh_url, oaipmh_repo, digest_login, opencast_url)

                # check dublincore catalogs of oaipmh
                oaipmh_episode_dc, oaipmh_series_dc = get_assets_of_oaipmh(oaipmh_record, episode_dc, series_dc,
                                                                           series_of_event, AssetType.DC, oaipmh_repo)

                if isinstance(oaipmh_episode_dc, Malformed):
                    error_collector.collect_errors(oaipmh_episode_dc, get_id(event))
                if isinstance(oaipmh_series_dc, Malformed):
                    error_collector.collect_errors(oaipmh_series_dc, get_id(event))

                # check acls of oaipmh
                oaipmh_episode_acl, oaipmh_series_acl = get_assets_of_oaipmh(oaipmh_record, episode_acl, series_acl,
                                                                             series_of_event, AssetType.ACL,
                                                                             oaipmh_repo)

                if isinstance(oaipmh_episode_acl, Malformed):
                    error_collector.collect_errors(oaipmh_episode_acl, get_id(event))
                if isinstance(oaipmh_series_acl, Malformed):
                    error_collector.collect_errors(oaipmh_series_acl, get_id(event))

            except RequestError as e:
                oaipmh_record = Malformed(errors=[e.error])
                error_collector.collect_errors(oaipmh_record, get_id(event))


def main():
    """
    Iterates over all series, and events and checks ACLs and/or dublincore catalogs, collects the error messages of all
    malformed elements
    print them out in the end.
    """

    opencast, tenants, exclude_tenants, https, digest_login, silent,  no_fancy_output, no_series_error, check, \
        results_dir = parse_args()

    url_builder = URLBuilder(opencast, https)
    check_settings = CheckSettings(check)

    progress_printer = ProgressPrinter(silent, no_fancy_output)
    error_collector = ErrorCollector()

    try:

        if not tenants:
            # get tenants
            progress_printer.print_message("Requesting tenants... ", 0, False, True)
            tenants = get_tenants(url_builder.get_base_url(None), digest_login)
            progress_printer.print_message("{} tenant(s) received.\n".format(len(tenants)), 0, True, False)

        if exclude_tenants:
            progress_printer.print_message("Filtering tenants... ", 0, False, True)
            tenants = [tenant for tenant in tenants if tenant not in exclude_tenants]
            progress_printer.print_message("{} tenant(s) remain.\n".format(len(tenants)), 0, True, False)

        tenants.sort()

        progress_printer.print_message('Starting checks for the following tenants: {}\n'.format(", ".join(tenants)), 0)

        for tenant in tenants:

            progress_printer.print_message("Starting check for tenant {}...\n".format(tenant), 0)
            error_collector.tenant(tenant)
            series_dc_map, series_acl_map, event_dc_map, event_acl_map = {}, {}, {}, {}

            opencast_url = url_builder.get_base_url(tenant)

            try:
                # SERIES #
                progress_printer.print_message("Requesting series... ", 1, False, True)
                series = get_series(opencast_url, digest_login)
                progress_printer.print_message("{} series received.\n".format(len(series)), 1, True, False)

                if series:

                    if check_settings.check_dc():
                        progress_printer.print_message("Starting check of dublincore catalogs of series... ", 2)
                        series_dc_map = check_assets_of_series(series, opencast_url, digest_login, AssetType.DC,
                                                               error_collector, progress_printer)

                    if check_settings.check_acl():
                        progress_printer.print_message("Starting check of ACLs of series... ", 2)
                        series_acl_map = check_assets_of_series(series, opencast_url, digest_login, AssetType.ACL,
                                                                error_collector, progress_printer)

                # EVENTS #
                progress_printer.print_message("Requesting events... ", 1, False, True)
                events = get_events(opencast_url, digest_login)
                progress_printer.print_message("{} event(s) received.\n".format(len(events)), 1, True, False)

                if events:

                    progress_printer.print_message("Starting check of series of events... ", 2)
                    event_series_map = check_series_of_events(events, series, error_collector, progress_printer,
                                                              no_series_error)

                    if check_settings.check_dc():
                        progress_printer.print_message("Starting check of dublincore catalogs of events... ", 2)
                        event_dc_map = check_assets_of_events(events, event_series_map, series_dc_map, opencast_url,
                                                              digest_login, AssetType.DC, error_collector,
                                                              progress_printer)

                    if check_settings.check_acl():
                        progress_printer.print_message("Starting check of ACLs of events... ", 2)
                        event_acl_map = check_assets_of_events(events, event_series_map, series_acl_map, opencast_url,
                                                               digest_login, AssetType.ACL, error_collector,
                                                               progress_printer)

                    if check_settings.check_oaipmh():
                        progress_printer.print_message("Filtering events... ", 1, False, True)
                        oaipmh_events = [event for event in events if published_to_oaipmh(event)]
                        progress_printer.print_message("{} of {} event(s) are published to OAIPMH.\n"
                                                       .format(len(oaipmh_events), len(events)), 1, True, False)

                        if oaipmh_events:
                            progress_printer.print_message("Starting check of OAIPMH... ", 2)
                            check_oaipmh(oaipmh_events, event_series_map, event_dc_map, event_acl_map, digest_login,
                                         error_collector, url_builder.get_base_url(None), progress_printer)

                progress_printer.print_message("...all checks for tenant {} finished. ".format(tenant), 0, False, True)

            except RequestError as err:
                error_collector.set_tenant_error(err.error)
                progress_printer.print_message("failed.\n", 0, True, False)
                progress_printer.print_message("...checks for tenant {} could not be completed: ".format(tenant), 0,
                                               False, True)

            error_collector.print_results_for_current_tenant()

        if len(tenants) > 1:
            error_collector.print_all_results()
        error_collector.write_to_file(results_dir)

    except RequestError as err:
        print(err.error)


if __name__ == '__main__':
    main()
