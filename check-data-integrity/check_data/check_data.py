"""
This module checks the data for errors and builds corresponding error messages.

(ACLs and Dublincores of series don't need to be checked because there can only ever be one, and if that's missing a
404 error will have been encountered.)
"""
from check_data.errors import missing, more, asset_without_series, more_series, series_not_found, asset_not_equal
from check_data.types import CatalogType, AssetType
from data_handling.compare_assets import compare_dc, compare_acl

def check_episode_asset_of_event(assets, elementtype, assettype, has_series):
    """
    Check episode ACL or dublincore of event for errors.

    :param assets: Episode ACLs or Dublincores of event
    :type assets: list
    :param elementtype: Event or OAIPMH
    :type elementtype: ElementType
    :param assettype: ACL or dublincore
    :type assettype: AssetType
    :param has_series: Whether the event belongs to a series
    :type has_series: bool
    :return: errors
    :rtype: list
    """

    errors = []

    if not assets:
        if assettype == AssetType.DC:
            errors.append(missing(elementtype, CatalogType.EPISODE, assettype)) # episode dc should never be missing
        elif assettype == AssetType.ACL:
            if not has_series:
                errors.append(missing(elementtype, CatalogType.EPISODE, assettype)) # episode acl can be missing if
                                                                                    # there's a series acl
    if len(assets) > 1:
        errors.append(more(elementtype, CatalogType.EPISODE, assettype))
    return errors

def check_series_asset_of_event(assets, has_series, elementtype, assettype):
    """
    Check series ACL or dublincore of event for errors.

    :param assets: Series ACLs or Dublincores of event
    :type assets: list
    :param has_series: Whether the event has a series
    :type has_series: bool
    :param elementtype: Event or OAIPMH
    :type elementtype: ElementType
    :param assettype: ACL or dublincore
    :type assettype: AssetType
    :return: errors
    :rtype: list
    """

    errors = []

    if has_series and not assets:
        errors.append(missing(elementtype, CatalogType.SERIES, assettype))

    if len(assets) > 1:
        errors.append(more(elementtype, CatalogType.SERIES, assettype))

    if assets and not has_series:
        errors.append(asset_without_series(elementtype, assettype))

    return errors

def check_series_of_event(series_of_event, has_series):
    """
    Check series of event for errors.

    :param series_of_event: Series found for event
    :type series_of_event: list
    :param has_series: Whether the event has a series
    :type has_series: bool
    :return: errors
    :rtype: list
    """

    errors = []

    if len(series_of_event) > 1:
        errors.append(more_series())
    if not series_of_event and has_series:
        errors.append(series_not_found())
    return errors

def check_asset_equality(asset1, asset2, elementtype, catalogtype, assettype):
    """
    Check whether two ACLs or dublincores are equal and return an error if not.

    :param asset1: ACL or dublincore
    :param asset2: ACL or dublincore
    :param elementtype: Series and Event or Event and OAIPMH
    :type elementtype: ElementType
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
        errors.append(asset_not_equal(elementtype, catalogtype, assettype))
    return errors