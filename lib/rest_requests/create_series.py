from rest_requests.request import get_request, post_request
from rest_requests.request_error import RequestError

NOT_FOUND = "404"


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
    Create a new series with a dublincore catalog (required) and an ACL (optional).

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param series_dc: Series dublincore catalog
    :type series_dc: ste
    :param series_acl: Series ACL (optional)
    :type series_acl: str
    :raise RequestError: If series could not be created
    """

    url = '{}/series/'.format(base_url)

    data = {'series': series_dc, 'acl': series_acl}

    post_request(url, digest_login, "/series/", data=data)
