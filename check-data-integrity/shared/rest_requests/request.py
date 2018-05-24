"""
This module offers different types of requests to a given URL.
"""

import requests
from requests.auth import HTTPDigestAuth

from shared.rest_requests.request_error import RequestError


def get_request(url, digest_login, element_description, asset_type_description=None, asset_description=None):
    """
    Make a get request to the given url with the given digest login. If the request fails with an error or a status
    code != 200, a Request Error with the error message /status code and the given descriptions is thrown.

    :param url: URL to make get request to
    :type url: str
    :param digest_login: Login data for digest authentication
    :type digest_login: DigestLogin
    :param element_description: Element description in case of errors, e.g. 'event', 'series', 'tenants' (required)
    :type element_description: str
    :param asset_type_description: Asset type description in case of errors, e.g. 'series', 'episode' (optional)
    :type asset_type_description: str
    :param asset_description: Asset description in case of errors, e.g. 'dublincore catalogs', 'ACL' (optional)
    :type asset_description: str
    :return: response
    :raise: RequestError
    """

    try:
        response = requests.get(url, auth=HTTPDigestAuth(digest_login.user, digest_login.password),
                                headers={"X-Requested-Auth": "Digest"})
    except Exception as e:
        raise RequestError.with_error(url, str(e), element_description, asset_type_description, asset_description)

    if response.status_code != 200:
        raise RequestError.with_statuscode(url, response.status_code, element_description, asset_type_description,
                                           asset_description)
    return response


def post_request(url, digest_login, element_description, asset_type_description=None, asset_description=None,
                 data=None, files=None):
    """
    Make a post request to the given url with the given digest login. If the request fails with an error or a status
    code != 200, a Request Error with the error message /status code and the given descriptions is thrown.

    :param url: URL to make post request to
    :type url: str
    :param digest_login: Login data for digest authentication
    :type digest_login: DigestLogin
    :param element_description: Element description in case of errors, e.g. 'event', 'series', 'tenants' (required)
    :type element_description: str
    :param asset_type_description: Asset type type description in case of errors, e.g. 'series', 'episode' (optional)
    :type asset_type_description: str
    :param asset_description: Asset description in case of errors, e.g. 'dublincore catalogs', 'ACL' (optional)
    :type asset_description: str
    :param data: Any data to attach to the request (optional)
    :type data: dict
    :param files: Any files to attach to the request (optional)
    :type files: dict
    :return: response
    :raise: RequestError
    """

    auth = HTTPDigestAuth(digest_login.user, digest_login.password)
    headers = {"X-Requested-Auth": "Digest"}

    try:
        response = requests.post(url, auth=auth, headers=headers, data=data, files=files)
    except Exception as e:
        raise RequestError.with_error(url, str(e), element_description, asset_type_description, asset_description)

    if response.status_code != 200:
        raise RequestError.with_statuscode(url, response.status_code, element_description, asset_type_description,
                                           asset_description)
    return response
