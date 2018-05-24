from shared.rest_requests.request import get_request
from shared.rest_requests.get_response_content import get_string_content


def get_mediapackage(base_url, digest_login, mp_id):
    """
    Get a mediapackage from the asset manager.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login data for digest authentication
    :type digest_login: DigestLogin
    :param mp_id: The ID of the mediapackage
    :type mp_id: str
    :return: A mediapackage definition in XML format
    :rtype str:
    """

    url = '{}/assets/episode/{}'.format(base_url, mp_id)

    response = get_request(url, digest_login, "mediapackage")

    mediapackage = get_string_content(response)

    return mediapackage
