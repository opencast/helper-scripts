import requests
from requests.auth import HTTPDigestAuth

from util.request_error import RequestError


def post_request(url, digest_login, description, data, files):

    auth = HTTPDigestAuth(digest_login.user, digest_login.password)
    headers = {"X-Requested-Auth": "Digest"}

    try:
        response = requests.post(url, auth=auth, headers=headers, data=data, files=files)
    except Exception as e:
        raise RequestError.with_error(description, url, str(e))

    if response.status_code != 200:
        raise RequestError.with_statuscode(description, url, response.status_code)
    return response


def get_request(url, digest_login, description):
    """
    Makes a get request to the given url with the given digest login.
    If the request fails, a Request Error with an error message containing the given asset description is thrown.

    :param url:
    :type url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :param description:
    :type description: str
    :return: response
    :raise: RequestError
    """

    try:
        response = requests.get(url, auth=HTTPDigestAuth(digest_login.user, digest_login.password),
                                headers={"X-Requested-Auth": "Digest"})
    except Exception as e:
        raise RequestError.with_error(description, url, str(e))

    if response.status_code != 200:
        raise RequestError.with_statuscode(description, url, response.status_code)
    return response
