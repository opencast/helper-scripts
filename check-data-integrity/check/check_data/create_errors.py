"""
This module contains methods to build error messages.
"""


def missing(element_description, asset_type_description, asset_description):
    """
    Formats error message for missing asset_description.

    :param element_description: SERIES, EVENT, OAIPMH
    :type element_description: ElementDescription
    :param asset_type_description: SERIES, EPISODE
    :type asset_type_description: AssetTypeDescription
    :param asset_description: DC, ACL
    :type asset_description: AssetDescription
    :return: error message
    :rtype: str
    """
    error = "{} missing the {} {}".format(element_description.unknown(), asset_type_description.singular(),
                                          asset_description.singular())

    return error


def more(element_description, asset_type_description, asset_description):
    """
    Formats error message for more than one asset_description of same type.

    :param element_description: EVENT, OAIPMH
    :type element_description: ElementDescription
    :param asset_type_description: SERIES, EPISODE
    :type asset_type_description: AssetTypeDescription
    :param asset_description: DC, ACL
    :type asset_description: AssetDescription
    :return: error message
    :rtype: str
    """
    error = "{} with more than one {} {}".format(element_description.unknown(), asset_type_description.singular(),
                                                 asset_description.singular())

    return error


def asset_not_equal(first_element_description, second_element_description, asset_type_description, asset_description):
    """
    Formats error message for nonequal assets.

    :param first_element_description: SERIES, EVENT or OAIPMH
    :type first_element_description: ElementDescription
    :param second_element_description: SERIES, EVENT or OAIPMH
    :type second_element_description: ElementDescription
    :param asset_type_description: SERIES, EPISODE
    :type asset_type_description: AssetTypeDescription
    :param asset_description: DC, ACL
    :type asset_description: AssetDescription
    :return: error message
    :rtype: str
    """
    error = "{} with a {} {} unequal with that of their {}".format(first_element_description.unknown(),
                                                                   asset_type_description.singular(),
                                                                   asset_description.singular(),
                                                                   second_element_description.singular())

    return error


def asset_without_series(element_description, asset_description):
    """
    Formats error message for series asset_description without series.

    :param element_description: EVENT, OAIPMH
    :type element_description: ElementDescription
    :param asset_description: DC, ACL
    :type asset_description: AssetDescription
    :return: error message
    :rtype: str
    """

    error = "{} with a series {} but no series".format(element_description.unknown(), asset_description.singular())

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


def parsing_error(element_description, asset_type_description, asset_description, error):
    """
    Formats error message for parsing error of asset_description.

    :param element_description: SERIES, EVENT, OAIPMH
    :type element_description: ElementDescription
    :param asset_type_description: SERIES, EPISODE
    :type asset_type_description: AssetTypeDescription
    :param asset_description: DC, ACL (but currently only ACL)
    :type asset_description: AssetDescription
    :param error: encountered error
    :type error: str
    :return: error message
    :rtype: str
    """

    error = "{} have a {} {} that could not be parsed: {}".format(element_description.unknown(),
                                                                  asset_type_description.singular(),
                                                                  asset_description.singular(), error)

    return error
