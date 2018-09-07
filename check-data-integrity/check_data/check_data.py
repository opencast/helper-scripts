"""
This module checks the data for errors and builds corresponding error messages.

(ACLs and Dublincores of series don't need to be checked because there can only ever be one, and if that's missing a
404 error will have been encountered.)
"""
from check_data.create_errors import missing, more, asset_without_series, more_series, series_not_found, \
    asset_not_equal, no_series
from check_data.malformed import Malformed
from check_data.types import CatalogType, AssetType
from data_handling.compare_assets import compare_dc, compare_acl


def check_episode_asset_of_event(assets, elementtype, assettype, series_of_event):
    """
    Check episode ACL or dublincore of event for errors.

    :param assets: Episode ACLs or Dublincores of event
    :type assets: list
    :param elementtype: Event or OAIPMH
    :type elementtype: ElementType
    :param assettype: ACL or dublincore
    :type assettype: AssetType
    :param series_of_event: Series of event
    :type series_of_event: dict or Malformed
    :return: errors
    :rtype: list
    """

    errors = []

    if not assets:
        if assettype == AssetType.DC:
            # episode dc should never be missing
            errors.append(missing(elementtype, CatalogType.EPISODE, assettype))
        elif assettype == AssetType.ACL:
            if not series_of_event or isinstance(series_of_event, Malformed):
                # episode acl can be missing if there's a series acl
                errors.append(missing(elementtype, CatalogType.EPISODE, assettype))

    if len(assets) > 1:
        errors.append(more(elementtype, CatalogType.EPISODE, assettype))
    return errors


def check_series_asset_of_event(assets, series_of_event, elementtype, assettype):
    """
    Check series ACL or dublincore of event for errors.

    :param assets: Series ACLs or Dublincores of event
    :type assets: list
    :param series_of_event: Series of event
    :type series_of_event: dict or Malformed
    :param elementtype: Event or OAIPMH
    :type elementtype: ElementType
    :param assettype: ACL or dublincore
    :type assettype: AssetType
    :return: errors
    :rtype: list
    """

    errors = []

    if series_of_event and not isinstance(series_of_event, Malformed) and not assets:
        errors.append(missing(elementtype, CatalogType.SERIES, assettype))

    if len(assets) > 1:
        errors.append(more(elementtype, CatalogType.SERIES, assettype))

    if assets and not series_of_event:
        errors.append(asset_without_series(elementtype, assettype))

    return errors


def check_series_of_event(series_of_event, has_series, no_series_error):
    """
    Check series of event for errors.

    :param series_of_event: Series found for event
    :type series_of_event: list
    :param has_series: Whether the event has a series
    :type has_series: bool
    :param no_series_error: Whether events without series are wrong
    :type no_series_error: bool
    :return: errors
    :rtype: list
    """

    errors = []

    if len(series_of_event) > 1:
        errors.append(more_series())
    if not series_of_event and has_series:
        errors.append(series_not_found())
    if not has_series and no_series_error:
        errors.append(no_series())
    return errors


def check_asset_equality(asset1, asset2, first_elementtype, second_elementtype, catalogtype, assettype):
    """
    Check whether two ACLs or dublincores are equal and return an error if not.

    :param asset1: ACL or dublincore
    :param asset2: ACL or dublincore
    :param first_elementtype: Series, Event or OAIPMH
    :type first_elementtype: ElementType
    :param second_elementtype: Series, Event or OAIPMH
    :type second_elementtype: ElementType
    :param catalogtype: Series or Episode
    :type catalogtype: CatalogType
    :param assettype: ACL or dublincore
    :type assettype: AssetType
    :return: errors
    :rtype: list
    """

    errors = []

    if assettype == AssetType.DC:
        asset_equal = compare_dc(asset1, asset2)
    else:
        asset_equal = compare_acl(asset1, asset2)

    if not asset_equal:
        errors.append(asset_not_equal(first_elementtype, second_elementtype, catalogtype, assettype))
    return errors
