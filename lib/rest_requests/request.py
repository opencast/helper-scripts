"""
This module offers different types of requests to a given URL.
"""
import os

import requests
from requests.auth import HTTPDigestAuth
from requests_toolbelt import MultipartEncoder

from rest_requests.request_error import RequestError


def get_request(url, digest_login, element_description, asset_type_description=None, asset_description=None,
                stream=False, headers=None):
    """
    Make a get request to the given url with the given digest login. If the request fails with an error or a status
    code != 200, a Request Error with the error message /status code and the given descriptions is thrown.

    :param url: URL to make get request to
    :type url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param element_description: Element description in case of errors, e.g. 'event', 'series', 'tenants'
    :type element_description: str
    :param asset_type_description: Asset type description in case of errors, e.g. 'series', 'episode'
    :type asset_type_description: str
    :param asset_description: Asset description in case of errors, e.g. 'Dublin Core catalogs', 'ACL'
    :type asset_description: str
    :param stream: Whether to stream response
    :type stream: bool
    :param headers: The headers to include in the request
    :type headers: dict
    :return: response
    :raise RequestError:
    """

    auth = HTTPDigestAuth(digest_login.user, digest_login.password)
    headers = headers if headers else {}
    headers["X-Requested-Auth"] = "Digest"

    try:
        response = requests.get(url, auth=auth, headers=headers, stream=stream)
    except Exception as e:
        raise RequestError.with_error(url, str(e), element_description, asset_type_description, asset_description)

    if response.status_code < 200 or response.status_code > 299:
        raise RequestError.with_status_code(url, str(response.status_code), element_description, asset_type_description,
                                            asset_description)
    return response


def post_request(url, digest_login, element_description, asset_type_description=None, asset_description=None,
                 data=None, files=None):
    """
    Make a post request to the given url with the given digest login. If the request fails with an error or a status
    code != 200, a Request Error with the error message /status code and the given descriptions is thrown.

    :param url: URL to make post request to
    :type url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param element_description: Element description in case of errors, e.g. 'event', 'series', 'tenants'
    :type element_description: str
    :param asset_type_description: Asset type type description in case of errors, e.g. 'series', 'episode'
    :type asset_type_description: str
    :param asset_description: Asset description in case of errors, e.g. 'Dublin Core catalogs', 'ACL'
    :type asset_description: str
    :param data: Any data to attach to the request
    :type data: dict
    :param files: Any files to attach to the request
    :type files: dict
    :return: response
    :raise RequestError:
    """

    auth = HTTPDigestAuth(digest_login.user, digest_login.password)
    headers = {"X-Requested-Auth": "Digest"}

    try:
        response = requests.post(url, auth=auth, headers=headers, data=data, files=files)
    except Exception as e:
        raise RequestError.with_error(url, str(e), element_description, asset_type_description, asset_description)

    if response.status_code < 200 or response.status_code > 299:
        raise RequestError.with_status_code(url, str(response.status_code), element_description, asset_type_description,
                                            asset_description)
    return response


def big_post_request(url, digest_login, element_description, asset_type_description=None, asset_description=None,
                     data=None, files=None):
    """
    Make a post request to the given url with the given digest login with potentially big files. If the request fails
    with an error or a status code != 200, a Request Error with the error message/status code and the given
    descriptions is thrown.

    :param url: URL to make post request to
    :type url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param element_description: Element description in case of errors, e.g. 'event', 'series', 'tenants'
    :type element_description: str
    :param asset_type_description: Asset type type description in case of errors, e.g. 'series', 'episode'
    :type asset_type_description: str
    :param asset_description: Asset description in case of errors, e.g. 'Dublin Core catalogs', 'ACL'
    :type asset_description: str
    :param data: Any data to attach to the request
    :type data: dict
    :param files: Any paths to potentially big files to attach to the request
    :type files: list
    :return: response
    :raise RequestError:
    """

    try:
        to_send = [(key, value) for key, value in data.items()]
        for file in files:
            to_send.append(('BODY', (os.path.basename(file), open(file, 'rb'))))  # make sure the files are sent last

        form = MultipartEncoder(to_send)

        auth = HTTPDigestAuth(digest_login.user, digest_login.password)
        headers = {"X-Requested-Auth": "Digest"}
        headers2 = {"X-Requested-Auth": "Digest", 'Content-Type': form.content_type}

        requests.post(url, headers=headers, auth=auth)  # make first request without body
        response = requests.post(url, headers=headers2, data=form, auth=auth)
    except Exception as e:
        print(e)
        raise RequestError.with_error(url, str(e), element_description, asset_type_description, asset_description)

    if response.status_code < 200 or response.status_code > 299:
        print(response.status_code)
        raise RequestError.with_status_code(url, str(response.status_code), element_description, asset_type_description,
                                            asset_description)
    return response


def put_request(url, digest_login, element_description, asset_type_description=None, asset_description=None,
                data=None, files=None):
    """
    Make a put request to the given url with the given digest login. If the request fails with an error or a status
    code != 200, a Request Error with the error message /status code and the given descriptions is thrown.

    :param url: URL to make put request to
    :type url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param element_description: Element description in case of errors, e.g. 'event', 'series', 'tenants'
    :type element_description: str
    :param asset_type_description: Asset type type description in case of errors, e.g. 'series', 'episode'
    :type asset_type_description: str
    :param asset_description: Asset description in case of errors, e.g. 'Dublin Core catalogs', 'ACL'
    :type asset_description: str
    :param data: Any data to attach to the request
    :type data: dict
    :param files: Any files to attach to the request
    :type files: dict
    :return: response
    :raise RequestError:
    """

    auth = HTTPDigestAuth(digest_login.user, digest_login.password)
    headers = {"X-Requested-Auth": "Digest"}

    try:
        response = requests.put(url, auth=auth, headers=headers, data=data, files=files)
    except Exception as e:
        raise RequestError.with_error(url, str(e), element_description, asset_type_description, asset_description)

    if response.status_code < 200 or response.status_code > 299:
        raise RequestError.with_status_code(url, str(response.status_code), element_description, asset_type_description,
                                            asset_description)
    return response
