from rest_requests.request import get_request, NOT_FOUND
from rest_requests.get_response_content import get_string_content
from rest_requests.request_error import RequestError


def get_media_package(base_url, digest_login, mp_id):
    """
    Get a media package from the asset manager.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param mp_id: The ID of the media package
    :type mp_id: str
    :return: A media package definition in XML format
    :rtype str:
    :raise RequestError:
    """

    url = '{}/assets/episode/{}'.format(base_url, mp_id)

    response = get_request(url, digest_login, "media package")

    media_package = get_string_content(response)

    return media_package


def media_package_exists(base_url, digest_login, mp_id):
    """
    Check if a media package exists.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param mp_id: The ID of the media package
    :type mp_id: str
    :return: true if it exists, false otherwise
    :rtype: bool
    :raise RequestError:
    """

    try:
        get_media_package(base_url, digest_login, mp_id)

    except RequestError as e:
        if e.has_status_code() and e.get_status_code() == NOT_FOUND:
            return False
        raise e

    return True
