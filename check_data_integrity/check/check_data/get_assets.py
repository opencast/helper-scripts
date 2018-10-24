"""
This module delivers assets (Dublin Core catalogs or acls) of events and series, by getting them from a request module
and performing checks to see if the data is consistent. If it is not, a Malformed object with the encountered
errors is returned instead.
"""
from check.check_data import create_errors
from check.check_data.check_data import check_episode_asset_of_event, \
    check_series_asset_of_event, check_asset_equality, check_series_of_event
from check.check_data.malformed import Malformed
from data_handling.elements import has_series
from data_handling.get_assets_from_oaipmh import get_assets_from_oaipmh
from data_handling.parse_acl import parse_acl
from data_handling.types import AssetDescription, ElementDescription, AssetTypeDescription
from rest_requests.asset_requests import get_asset_of_series_from_rest, get_assets_of_event_from_rest
from rest_requests.request_error import RequestError


def parse_for_comparison(asset, element_description, asset_type_description, asset_description):
    """
    Parses the assets of a certain type into the same format so that they can be compared later. Currently only
    necessary for ACLs. Returns a Malformed object if there is an error during parsing.

    :param asset:
    :param element_description: Series, Event or OAIPMH
    :type element_description: ElementDescription
    :param asset_type_description: Series or Episode
    :type asset_type_description: AssetTypeDescription
    :param asset_description: ACL or DC
    :type asset_description: AssetDescription
    :return: parsed asset (ACL), unchanged asset (DC) or Malformed
    :rtype: dict, ElementTree.Element, Malformed
    """
    if asset_description == AssetDescription.DC:
        return asset  # no parsing necessary, all Dublin Core catalogs are already in the same format
    else:
        try:
            asset = parse_acl(asset)  # parsing necessary since ACLs can be in a different format
            return asset
        except Exception as e:
            error = create_errors.parsing_error(element_description, asset_type_description, asset_description, str(e))
            return Malformed(errors=[error])


def get_asset_of_series(series, opencast_url, digest_login, asset_description):
    """
    Get series ACL and or Dublin Core catalog from series and check if valid. If there are any errors, a Malformed
    object containing the errors is returned instead.

    :param series:
    :type series: dict
    :param opencast_url:
    :type opencast_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :param asset_description: ACL or DC
    :type asset_description: AssetDescription
    :return: Series asset or Malformed
    """

    try:
        series_asset = get_asset_of_series_from_rest(series, opencast_url, digest_login, asset_description)
    except RequestError as e:
        return Malformed(errors=[e.error])

    series_asset = parse_for_comparison(series_asset, ElementDescription.SERIES, AssetTypeDescription.SERIES,
                                        asset_description)

    return series_asset


def get_assets_of_event(event, opencast_url, digest_login, series_of_event, series_asset_of_series, asset_description):
    """
    Get episode and series ACLs and or Dublin Core catalog from event and check if valid. If there are any errors, two
    Malformed objects containing the errors are returned instead.

    :param event:
    :param opencast_url:
    :type opencast_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :param series_of_event:
    :type series_of_event: dict or Malformed
    :param series_asset_of_series:
    :param asset_description:
    :type asset_description: AssetDescription
    :return: Episode asset, series asset or Malformed*2 or None*2
    """

    try:
        episode_assets, series_assets = get_assets_of_event_from_rest(event, opencast_url, digest_login,
                                                                      asset_description)
    except RequestError as e:
        return Malformed(errors=[e.error]), Malformed(errors=[e.error])

    errors = check_episode_asset_of_event(episode_assets, ElementDescription.EVENT, asset_description, series_of_event)

    if errors:
        episode_asset = Malformed(errors=errors)
    else:
        episode_asset = episode_assets[0] if episode_assets else None

    if episode_asset and not isinstance(episode_asset, Malformed):
        episode_asset = parse_for_comparison(episode_asset, ElementDescription.EVENT, AssetTypeDescription.EPISODE,
                                             asset_description)

    errors = check_series_asset_of_event(series_assets, series_of_event, ElementDescription.EVENT, asset_description)

    if errors:
        series_asset = Malformed(errors=errors)
    else:
        series_asset = series_assets[0] if series_assets else None

    if series_asset and not isinstance(series_asset, Malformed):
        series_asset = parse_for_comparison(series_asset, ElementDescription.EVENT, AssetTypeDescription.SERIES,
                                            asset_description)

    if not isinstance(series_asset, Malformed) and not isinstance(series_asset_of_series, Malformed):

        errors = check_asset_equality(series_asset, series_asset_of_series, ElementDescription.EVENT,
                                      ElementDescription.SERIES, AssetTypeDescription.SERIES, asset_description)
        if errors:
            series_asset = Malformed(errors=errors)

    return episode_asset, series_asset


def get_assets_of_oaipmh(oaipmh_record, original_episode_asset, original_series_asset, series_of_event,
                         asset_description, repository):
    """
    Get episode and series ACLs or Dublin Cores from an oaipmh record and check for errors. Also check whether they
    match the ACLs and Dublin Cores from the event. If there are any errors, two Malformed objects containing the
    errors are returned instead.

    :param oaipmh_record:
    :type oaipmh_record: ElementTree.Element
    :param original_episode_asset:
    :param original_series_asset:
    :param series_of_event:
    :type series_of_event: dict or Malformed
    :param asset_description: ACL or Dublin Core
    :type asset_description: AssetDescription
    :param repository: OAIPMH repository id
    :type repository: str
    :return: Episode asset, series asset or Malformed*2 or None*2
    """

    episode_assets, series_assets = get_assets_from_oaipmh(oaipmh_record, asset_description)

    # check episode asset
    errors = check_episode_asset_of_event(episode_assets, ElementDescription.OAIPMH.format(repository),
                                          asset_description, series_of_event)

    if errors:
        episode_asset = Malformed(errors=errors)
    else:
        episode_asset = episode_assets[0] if episode_assets else None

    if episode_asset and not isinstance(episode_asset, Malformed):
        episode_asset = parse_for_comparison(episode_asset, ElementDescription.OAIPMH.format(repository),
                                             AssetTypeDescription.EPISODE, asset_description)

    if not isinstance(episode_asset, Malformed) and not isinstance(original_episode_asset, Malformed):

        errors = check_asset_equality(episode_asset, original_episode_asset, ElementDescription.EVENT,
                                      ElementDescription.OAIPMH.format(repository), AssetTypeDescription.EPISODE,
                                      asset_description)
        if errors:
            episode_asset = Malformed(errors=errors)

    # check series asset
    errors = check_series_asset_of_event(series_assets, series_of_event, ElementDescription.OAIPMH.format(repository),
                                         asset_description)

    if errors:
        series_asset = Malformed(errors=errors)
    else:
        series_asset = series_assets[0] if series_assets else None

    if series_asset and not isinstance(series_asset, Malformed):
        series_asset = parse_for_comparison(series_asset, ElementDescription.OAIPMH.format(repository),
                                            AssetTypeDescription.SERIES, asset_description)

    if not isinstance(series_asset, Malformed) and not isinstance(original_series_asset, Malformed):

        errors = check_asset_equality(series_asset, original_series_asset, ElementDescription.EVENT,
                                      ElementDescription.OAIPMH.format(repository), AssetTypeDescription.SERIES,
                                      asset_description)
        if errors:
            series_asset = Malformed(errors=errors)

    return episode_asset, series_asset


def get_series_of_event(series, event, no_series_error):
    """
    Get series of event from a list of series and check if valid. If there are any errors, a Malformed object
    containing the errors is returned instead.

    :param series: All series
    :type series: list
    :param event:
    :type event: dict
    :param no_series_error: Whether events without series are considered malformed
    :type no_series_error: bool
    :return: Series, Malformed or None
    :rtype: dict, Malformed or None
    """

    series_of_event = [serie for serie in series if
                       ("series" in event and serie["id"] == event["series"]["id"])]

    errors = check_series_of_event(series_of_event, has_series(event), no_series_error)

    if errors:
        return Malformed(errors=errors)

    return series_of_event[0] if series_of_event else None
