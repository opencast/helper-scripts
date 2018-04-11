"""
This module contains methods to build error messages.
"""

from util.enum import enum

Errors = enum(
    MISSING = "{} is missing the {} {}",
    MORE = "{} has more than one {} {}",

    ASSET_NOT_EQUAL="{} have nonequal {} {}s",

    ASSET_WITHOUT_SERIES="{} has series {} but no series",

    MORE_SERIES = "Event has more than one series",
    SERIES_NOT_FOUND = "Series of event could not be found",

    PARSING_ERROR = "{} {} of {} could not be parsed: {}"
)

def missing(elementtype, catalogtype, assettype):
    """
    Formats error message for missing asset.

    :param elementtype: SERIES, EVENT, OAIPMH
    :type elementtype: ElementType
    :param catalogtype: SERIES, EPISODE
    :type catalogtype: CatalogType
    :param assettype: DC, ACL
    :type assettype: AssetType
    :return: formatted error message
    :rtype: str
    """
    return Errors.MISSING.format(elementtype, catalogtype, assettype)

def more(elementtype, catalogtype, assettype):
    """
    Formats error message for more than one asset of same type.

    :param elementtype: EVENT, OAIPMH
    :type elementtype: ElementType
    :param catalogtype: SERIES, EPISODE
    :type catalogtype: CatalogType
    :param assettype: DC, ACL
    :type assettype: AssetType
    :return: formatted error message
    :rtype: str
    """
    return Errors.MORE.format(elementtype, catalogtype, assettype)

def asset_not_equal(elementtype, catalogtype, assettype):
    """
    Formats error message for nonequal assets.

    :param elementtype: SERIES_EVENT, EVENT_OAIPMH
    :type elementtype: ElementType
    :param catalogtype: SERIES, EPISODE
    :type catalogtype: CatalogType
    :param assettype: DC, ACL
    :type assettype: AssetType
    :return: formatted error message
    :rtype: str
    """

    return Errors.ASSET_NOT_EQUAL.format(elementtype, catalogtype, assettype)

def asset_without_series(elementtype, assettype):
    """
    Formats error message for series asset without series.

    :param elementtype: EVENT, OAIPMH
    :type elementtype: ElementType
    :param assettype: DC, ACL
    :type assettype: AssetType
    :return: formatted error message
    :rtype: str
    """
    return Errors.ASSET_WITHOUT_SERIES.format(elementtype, assettype)

def more_series():
    """
    Formats error message for event with more than one series.

    :return: formatted error message
    :rtype: str
    """
    return Errors.MORE_SERIES

def series_not_found():
    """
    Formats error message for event with missing series.

    :return: formatted error message
    :rtype: str
    """
    return Errors.SERIES_NOT_FOUND

def parsing_error(elementtype, catalogtype, assettype, error):
    """
    Formats error message for parsing error of asset.

    :param elementtype: SERIES, EVENT, OAIPMH
    :type elementtype: ElementType
    :param catalogtype: SERIES, EPISODE
    :type catalogtype: CatalogType
    :param assettype: DC, ACL (but currently only ACL)
    :type assettype: AssetType
    :return: formatted error message
    :rtype: str
    """

    return Errors.PARSING_ERROR.format(catalogtype, assettype, elementtype, error)