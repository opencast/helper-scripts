import requests
from requests.auth import HTTPDigestAuth

from rest_requests.request_error import RequestError


def __get_request(url, digest_login, element_description, catalog_description = None, asset_description= None):
    '''
    Makes a get request to the given url with the given digest login.
    If the request fails, a Request Error with an error message containing the given asset description is thrown.

    :param url:
    :type url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :param asset_description:
    :type asset_description: str
    :return: response
    :raise: RequestError
    '''

    try:
        response = requests.get(url, auth=HTTPDigestAuth(digest_login.user, digest_login.password),
                                headers={"X-Requested-Auth": "Digest"})
    except Exception as e:
        raise RequestError.with_error(url, str(e), element_description, catalog_description, asset_description)

    if (response.status_code != 200):
        raise RequestError.with_statuscode(url, response.status_code, element_description, catalog_description, asset_description)
    return response