from datetime import datetime
from datetime import timedelta

from rest_requests.get_response_content import get_string_content
from rest_requests.request import get_request


def sign_url(digest_login, server_url, url_to_sign):
    """
    Get a URL signed for 2 hours.

    :param digest_login: The login credentials for digest auth
    :type digest_login: DigestLogin
    :param server_url: The server URL
    :type server_url: str
    :param url_to_sign: The url to be signed
    :type url_to_sign: str
    :return: The signed URL
    :rtype: str
    :raise RequestError:
    """

    now = datetime.now()
    two_hours = timedelta(hours=2)
    two_hours_from_now = now + two_hours
    two_hours_from_now_timestamp = int(two_hours_from_now.timestamp())

    url = '{}/signing/sign?baseUrl={}&validUntil={}'.format(server_url, url_to_sign, two_hours_from_now_timestamp)
    response = get_request(url, digest_login, "signed URL")
    return get_string_content(response)


def accepts_url(digest_login, server_url, url_to_sign):
    """
    Checks if a URL can be signed.

    :param digest_login: The login credentials for digest auth
    :type digest_login: DigestLogin
    :param server_url: The server URL
    :type server_url: str
    :param url_to_sign: The url to check
    :type url_to_sign: str
    :return: If the URL can be signed.
    :rtype: bool
    :raise RequestError:
    """

    url = '{}/signing/accepts?baseUrl={}'.format(server_url, url_to_sign)
    response = get_request(url, digest_login, "URL signing check")
    return get_string_content(response) == "true"
