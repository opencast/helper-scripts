import json

from rest_requests.get_response_content import get_json_content, get_xml_content
from rest_requests.request import get_request, post_request, NOT_FOUND
from rest_requests.request_error import RequestError


def series_exists(base_url, digest_login, series_id):
    """
    Check if series of media package to be recovered still exists.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param series_id: ID of the series to be checked
    :type series_id: str
    :return: True if the series still exists, False otherwise
    :rtype: bool
    :raise RequestError: If an error other than 404 occurs
    """

    url = '{}/series/{}.json'.format(base_url, series_id)

    try:
        get_request(url, digest_login, "/series/{id}.json")

    except RequestError as e:

        if e.has_status_code() and e.get_status_code() == NOT_FOUND:
            return False
        raise e

    return True


def create_series(base_url, digest_login, series_dc, series_acl=None):
    """
    Create a new series with a Dublin Core catalog (required) and an ACL (optional).

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param series_dc: Series Dublin Core catalog
    :type series_dc: ste
    :param series_acl: Series ACL
    :type series_acl: str
    :raise RequestError: If series could not be created
    """

    url = '{}/series/'.format(base_url)

    data = {'series': series_dc, 'acl': series_acl}

    post_request(url, digest_login, "/series/", data=data)


def get_all_series(base_url, digest_login):
    """
    Get all series.

    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :return: list of series
    :rtype: list
    :raise RequestError:
    """

    url = '{}/series/allSeriesIdTitle.json'.format(base_url)
    response = get_request(url, digest_login, "series")
    return get_json_content(response)["series"]


def get_dc_of_series(series_id, base_url, digest_login, element_description="series",
                     asset_type_description=None, asset_description=None):
    """
    Get the series Dublin Core catalog for a given series.

    :param series_id: The series id
    :type series_id: str
    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :return: The series Dublin Core catalog
    :rtype: ElementTree.Element
    :raise RequestError:
    """

    url = '{}/series/{}.xml'.format(base_url, series_id)
    response = get_request(url, digest_login, element_description, asset_type_description, asset_description)
    series_dc = get_xml_content(response)
    return series_dc


def get_acl_of_series(series_id, base_url, digest_login, element_description="series",
                     asset_type_description=None, asset_description=None):
    """
    Get the series ACL for a given series.

    :param series_id: The series id
    :type series_id: str
    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :return: The series ACL
    :rtype: dict
    :raise RequestError:
    """

    url = "{}/series/{}/acl.json".format(base_url, series_id)
    response = get_request(url, digest_login, element_description, asset_type_description, asset_description)
    return get_json_content(response)


def update_acl_of_series(series_id, base_url, digest_login, acl):
    """
    Update acl of series
    :param series_id: The series id
    :type series_id: str
    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param acl: The series ACL
    :type acl: dict
    :return:
    """

    url = "{}/series/{}/accesscontrol".format(base_url, series_id)
    data = {'override': "false", 'acl': json.dumps(acl)}
    post_request(url, digest_login, "series", data=data)
