"""
This module checks the data for errors and builds corresponding error messages.

(ACLs and Dublin Core catalogs of series don't need to be checked because there can only ever be one, and if that's
missing a 404 error will have been encountered.)
"""
from check.check_data.create_errors import missing, more, asset_without_series, more_series, \
    series_not_found, no_series, asset_not_equal
from check.check_data.malformed import Malformed
from data_handling.compare_assets import compare_dc, compare_acl
from data_handling.types import AssetDescription, AssetTypeDescription


def check_episode_asset_of_event(assets, element_description, asset_description, series_of_event):
    """
    Check episode ACL or Dublin Core of event for errors.

    :param assets: Episode ACLs or Dublin Cores of event
    :type assets: list
    :param element_description: Event or OAIPMH
    :type element_description: ElementDescription
    :param asset_description: ACL or Dublin Core
    :type asset_description: AssetDescription
    :param series_of_event: Series of event
    :type series_of_event: dict or Malformed
    :return: errors
    :rtype: list
    """

    errors = []

    if not assets:
        if asset_description == AssetDescription.DC:
            # episode dc should never be missing
            errors.append(missing(element_description, AssetTypeDescription.EPISODE, asset_description))
        elif asset_description == AssetDescription.ACL:
            if not series_of_event or isinstance(series_of_event, Malformed):
                # episode acl can be missing if there's a series acl
                errors.append(missing(element_description, AssetTypeDescription.EPISODE, asset_description))

    if len(assets) > 1:
        errors.append(more(element_description, AssetTypeDescription.EPISODE, asset_description))
    return errors


def check_series_asset_of_event(assets, series_of_event, element_description, asset_description):
    """
    Check series ACL or Dublin Core of event for errors.

    :param assets: Series ACLs or Dublin Cores of event
    :type assets: list
    :param series_of_event: Series of event
    :type series_of_event: dict or Malformed
    :param element_description: Event or OAIPMH
    :type element_description: ElementDescription
    :param asset_description: ACL or Dublin Core
    :type asset_description: AssetDescription
    :return: errors
    :rtype: list
    """

    errors = []

    if series_of_event and not isinstance(series_of_event, Malformed) and not assets:
        errors.append(missing(element_description, AssetTypeDescription.SERIES, asset_description))

    if len(assets) > 1:
        errors.append(more(element_description, AssetTypeDescription.SERIES, asset_description))

    if assets and not series_of_event:
        errors.append(asset_without_series(element_description, asset_description))

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


def check_asset_equality(asset1, asset2, first_element_description, second_element_description, asset_type_description,
                         asset_description):
    """
    Check whether two ACLs or Dublin Cores are equal and return an error if not.

    :param asset1: ACL or Dublin Core
    :param asset2: ACL or Dublin Core
    :param first_element_description: Series, Event or OAIPMH
    :type first_element_description: ElementDescription
    :param second_element_description: Series, Event or OAIPMH
    :type second_element_description: ElementDescription
    :param asset_type_description: Series or Episode
    :type asset_type_description: AssetTypeDescription
    :param asset_description: ACL or Dublin Core
    :type asset_description: AssetDescription
    :return: errors
    :rtype: list
    """

    errors = []

    if asset_description == AssetDescription.DC:
        asset_equal = compare_dc(asset1, asset2)
    else:
        asset_equal = compare_acl(asset1, asset2)

    if not asset_equal:
        errors.append(asset_not_equal(first_element_description, second_element_description, asset_type_description,
                                      asset_description))
    return errors
