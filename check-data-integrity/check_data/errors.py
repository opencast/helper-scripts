"""
This module contains methods to build error messages.
"""


def missing(elementtype, catalogtype, assettype):
    """
    Formats error message for missing asset.

    :param elementtype: SERIES, EVENT, OAIPMH
    :type elementtype: ElementType
    :param catalogtype: SERIES, EPISODE
    :type catalogtype: CatalogType
    :param assettype: DC, ACL
    :type assettype: AssetType
    :return: error message
    :rtype: str
    """
    error = "{} missing the {} {}".format(elementtype.unknown, catalogtype.singular, assettype.singular)

    return error

def more(elementtype, catalogtype, assettype):
    """
    Formats error message for more than one asset of same type.

    :param elementtype: EVENT, OAIPMH
    :type elementtype: ElementType
    :param catalogtype: SERIES, EPISODE
    :type catalogtype: CatalogType
    :param assettype: DC, ACL
    :type assettype: AssetType
    :return: error message
    :rtype: str
    """
    error = "{} with more than one {} {}".format(elementtype.unknown, catalogtype.singular, assettype.singular)

    return error

def asset_not_equal(first_elementtype, second_elementtype, catalogtype, assettype):
    """
    Formats error message for nonequal assets.

    :param first_elementtype: SERIES, EVENT or OAIPMH
    :type first_elementtype: ElementType
    :param second_elementtype: SERIES, EVENT or OAIPMH
    :type second_elementtype: ElementType
    :param catalogtype: SERIES, EPISODE
    :type catalogtype: CatalogType
    :param assettype: DC, ACL
    :type assettype: AssetType
    :return: error message
    :rtype: str
    """
    error = "{} with a {} {} unequal with that of their {}".format(first_elementtype.unknown,
                                                                         catalogtype.singular, assettype.singular,
                                                                         second_elementtype.singular)

    return error

def asset_without_series(elementtype, assettype):
    """
    Formats error message for series asset without series.

    :param elementtype: EVENT, OAIPMH
    :type elementtype: ElementType
    :param assettype: DC, ACL
    :type assettype: AssetType
    :return: error message
    :rtype: str
    """

    error = "{} with a series {} but no series".format(elementtype.unknown, assettype.singular)

    return error

def more_series():
    """
    Formats error message for event with more than one series.

    :return: error message
    :rtype: strr
    """

    error = "event(s) with more than one series"

    return error

def series_not_found():
    """
    Formats error message for event with missing series.

    :return: error message
    :rtype: str
    """

    error = "event(s) where their series could not be found"

    return error

def no_series():
    """
    Formats error message for event with missing series.

    :return: error message
    :rtype: str
    """

    error = "event(s) without a series"
    return error

def parsing_error(elementtype, catalogtype, assettype, error):
    """
    Formats error message for parsing error of asset.

    :param elementtype: SERIES, EVENT, OAIPMH
    :type elementtype: ElementType
    :param catalogtype: SERIES, EPISODE
    :type catalogtype: CatalogType
    :param assettype: DC, ACL (but currently only ACL)
    :type assettype: AssetType
    :return: error message
    :rtype: str
    """

    error = "{} have a {} {} that could not be parsed: {}".format(elementtype.unknown, catalogtype.singular,
                                                                  assettype.singular, error)

    return error