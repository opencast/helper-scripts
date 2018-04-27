"""
This module delivers associated elements of events and series, e.g. dublincore catalogs or acls, by getting them
from a request module and performing checks to see if the data is wellformed. If it is not, a Malformed object with the
encountered errors is returned instead.
"""
from check_data import errors
from check_data.check_data import check_episode_asset_of_event, check_series_asset_of_event, check_asset_equality, \
    check_series_of_event
from check_data.malformed import Malformed
from check_data.types import ElementType, AssetType, CatalogType
from data_handling.element_util import has_series
from data_handling.get_assets_from_oaipmh import get_assets_from_oaipmh
from data_handling.parse_acl import parse_acl
from rest_requests.asset_requests import get_asset_of_series_from_rest, get_assets_of_event_from_rest
from rest_requests.request_error import RequestError

def __parse_for_comparison(asset, elementtype, catalogtype, assettype):
    """
    Parses the assets of a certain type into the same format so that they can be compared later. Currently only
    necessary for ACLs. Returns a Malformed object if there is an error during parsing.

    :param asset:
    :param elementtype: Series, Event or OAIPMH
    :type elementtype: ElementType
    :param catalogtype: Series or Episode
    :type catalogtype: CatalogType
    :param assettype: ACL or DC
    :type assettype: AssetType
    :return: parsed asset (ACL), unchanged asset (DC) or Malformed
    :rtype: dict, ElementTree.Element, Malformed
    """
    if assettype == AssetType.DC:
        return asset  # no parsing necessary, all dublincore catalogs are already in the same format
    else:
        try:
            asset = parse_acl(asset)  # parsing necessary since acls can be in a different format
            return asset
        except Exception as e:
            error = errors.parsing_error(elementtype, catalogtype, assettype, str(e))
            return Malformed(errors=[error])

def get_asset_of_series(series, opencast_url, digest_login, assettype):
    """
    Get series ACL and or dublincore from series and check if valid. If there are any errors, a Malformed
    object containing the errors is returned instead.

    :param series:
    :type series: dict
    :param opencast_url:
    :type opencast_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :return: Series asset or Malformed
    """

    try:
        series_asset = get_asset_of_series_from_rest(series, opencast_url, digest_login, assettype)
    except RequestError as e:
        return Malformed(errors=[e.error])

    series_asset = __parse_for_comparison(series_asset, ElementType.SERIES, CatalogType.SERIES, assettype)

    return series_asset

def get_assets_of_event(event, opencast_url, digest_login, series_of_event, series_asset_of_series, assettype):
    """
    Get episode and series ACLs and or dublincore from event and check if valid. If there are any errors, two Malformed
    objects containing the errors are returned instead.

    :param event:
    :param opencast_url:
    :type opencast_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :param series_of_event:
    :type series_of_event: dict or Malformed
    :param series_asset_of_series:
    :param assettype:
    :type assettype: AssetType
    :return: Episode asset, series asset or Malformed*2 or None*2
    """

    try:
        episode_assets, series_assets = get_assets_of_event_from_rest(event, opencast_url, digest_login, assettype)
    except RequestError as e:
        return Malformed(errors=[e.error]), Malformed(errors=[e.error])

    errors = check_episode_asset_of_event(episode_assets, ElementType.EVENT, assettype, series_of_event)

    if errors:
        episode_asset = Malformed(errors=errors)
    else:
        episode_asset = episode_assets[0] if episode_assets else None

    if episode_asset and not isinstance(episode_asset, Malformed):
        episode_asset = __parse_for_comparison(episode_asset, ElementType.EVENT, CatalogType.EPISODE, assettype)

    errors = check_series_asset_of_event(series_assets, series_of_event, ElementType.EVENT, assettype)

    if errors:
        series_asset = Malformed(errors=errors)
    else:
        series_asset = series_assets[0] if series_assets else None

    if series_asset and not isinstance(series_asset, Malformed):
        series_asset = __parse_for_comparison(series_asset, ElementType.EVENT, CatalogType.SERIES, assettype)

    if not isinstance(series_asset, Malformed) and not isinstance(series_asset_of_series, Malformed):

        errors = check_asset_equality(series_asset, series_asset_of_series, ElementType.EVENT, ElementType.SERIES, CatalogType.SERIES,
                                      assettype)
        if errors:
            series_asset = Malformed(errors=errors)

    return episode_asset, series_asset

def get_assets_of_oaipmh(oaipmh_record, original_episode_asset, original_series_asset, series_of_event, assettype, repository):
    """
    Get episode and series ACLs or dublincores from an oaipmh record and check for errors. Also check whether they match
    the ACLs and dublincores from the event. If there are any errors, two Malformed objects containing the errors are
    returned instead.

    :param oaipmh_record:
    :type oaipmh_record: ElementTree.Element
    :param original_episode_asset:
    :param original_series_asset:
    :param series_of_event:
    :type series_of_event: bool
    :param assettype: ACL or dublincore
    :type assettype: AssetType
    :return: Episode asset, series asset or Malformed*2 or None*2
    """

    episode_assets, series_assets = get_assets_from_oaipmh(oaipmh_record, assettype)

    # check episode asset
    errors = check_episode_asset_of_event(episode_assets, ElementType.OAIPMH.format(repository), assettype, series_of_event)

    if errors:
        episode_asset = Malformed(errors=errors)
    else:
        episode_asset = episode_assets[0] if episode_assets else None

    if episode_asset and not isinstance(episode_asset, Malformed):
        episode_asset = __parse_for_comparison(episode_asset, ElementType.OAIPMH.format(repository), CatalogType.EPISODE, assettype)

    if not isinstance(episode_asset, Malformed) and not isinstance(original_episode_asset, Malformed):

        errors = check_asset_equality(episode_asset, original_episode_asset, ElementType.EVENT, ElementType.OAIPMH.format(repository), CatalogType.EPISODE, assettype)
        if errors:
            episode_asset = Malformed(errors=errors)

    # check series asset
    errors = check_series_asset_of_event(series_assets, series_of_event, ElementType.OAIPMH.format(repository), assettype)

    if errors:
        series_asset = Malformed(errors=errors)
    else:
        series_asset = series_assets[0] if series_assets else None

    if series_asset and not isinstance(series_asset, Malformed):
        series_asset = __parse_for_comparison(series_asset, ElementType.OAIPMH.format(repository), CatalogType.SERIES, assettype)

    if not isinstance(series_asset, Malformed) and not isinstance(original_series_asset, Malformed):

        errors = check_asset_equality(series_asset, original_series_asset, ElementType.EVENT, ElementType.OAIPMH.format(repository), CatalogType.SERIES, assettype)
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
    :return: Series, Malformed or None
    :rtype: dict, Malformed or None
    """

    series_of_event = [serie for serie in series if
                            ("series" in event and serie["id"] == event["series"]["id"])]

    errors = check_series_of_event(series_of_event, has_series(event), no_series_error)

    if errors:
        return Malformed(errors=errors)

    return series_of_event[0] if series_of_event else None