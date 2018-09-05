import requests
from requests.auth import HTTPDigestAuth

from script.requests.util.request_error import RequestError


def post_request(url, digest_login, description, data=None, files=None):
    """
    Make a post request to the given url with the given digest login.
    If the request fails, a Request Error with an error message containing the given description is thrown.

    :param url: The URL to send the request to
    :type url: str
    :param digest_login: The login data for digest authentication
    :type digest_login: DigestLogin
    :param description: The description of the requested resource in case of an error
    :type description: str
    :param data: The data to post (optional)
    :type data: dict or None
    :param files: The files to post (optional)
    :type files: dict or None
    :return: The response
    :raise: RequestError
    """

    auth = HTTPDigestAuth(digest_login.user, digest_login.password)
    headers = {"X-Requested-Auth": "Digest"}

    try:
        response = requests.post(url, auth=auth, headers=headers, data=data, files=files)
    except Exception as e:
        raise RequestError.with_error(description, url, str(e))

    if response.status_code < 200 or response.status_code > 299:
        raise RequestError.with_status_code(description, url, response.status_code)
    return response


def get_request(url, digest_login, description):
    """
    Make a get request to the given url with the given digest login.
    If the request fails, a Request Error with an error message containing the given description is thrown.

    :param url: The URL to send the request to
    :type url: str
    :param digest_login: The login data for digest authentication
    :type digest_login: DigestLogin
    :param description: The description of the requested resource in case of an error
    :type description: str
    :return: The response
    :raise: RequestError
    """

    try:
        response = requests.get(url, auth=HTTPDigestAuth(digest_login.user, digest_login.password),
                                headers={"X-Requested-Auth": "Digest"})
    except Exception as e:
        raise RequestError.with_error(description, url, str(e))

    if response.status_code != 200:
        raise RequestError.with_status_code(description, url, response.status_code)
    return response
