"""
This module provides methods to make some basic requests to the opencast REST API.
"""
from data_handling.elements import get_id
from rest_requests.request import get_request
from rest_requests.get_response_content import get_json_content

JAVA_MAX_INT = 2147483647


def get_tenants(base_url, digest_login):
    """
    Return a sorted list of unique tenant IDs

    :param base_url: The URL to an opencast instance
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :return: tenant ids
    :raise RequestError:
    """

    url = '{}/org/all.json'.format(base_url)

    response = get_request(url, digest_login, "tenants")

    json_content = get_json_content(response)

    if isinstance(json_content["organizations"]["organization"], list):
        tenants = [org["id"] for org in (json_content["organizations"])["organization"]]
        tenants = sorted(set(tenants))
    else:
        tenants = [json_content["organizations"]["organization"]["id"]]
    return tenants


def get_series(base_url, digest_login):
    """
    Return all series of one tenant.

    :param base_url: The URL to an opencast instance including the tenant
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :return: series
    :rtype: list
    :raise RequestError:
    """

    all_series = []
    offset = 0
    limit = 1000

    while True:
        series = __get_series(base_url, digest_login, offset, limit)
        if series['count'] == 0:
            return all_series
        all_series = all_series + series["results"]
        offset += limit


def __get_series(base_url, digest_login, offset=0, limit=100):
    """
    Return series by offset and limit.

    :param base_url: The URL to an opencast instance including the tenant
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param offset: The pagination offset
    :type offset: int
    :param limit: The pagination limit
    :type limit: int
    :return: series
    :rtype: dict
    :raise RequestError:
    """

    url = '{}/admin-ng/series/series.json?limit={}&offset={}'.format(base_url, limit, offset)
    response = get_request(url, digest_login, "series")
    return get_json_content(response)


def get_all_events(base_url, digest_login):
    """
    Return all events.

    :param base_url: The URL to an opencast instance including the tenant
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :return: events
    :raise RequestError:
    """

    all_events = []
    offset = 0
    limit = 1000
    while True:
        events = __get_events(base_url, digest_login, offset, limit)
        if events['count'] == 0:
            return all_events
        all_events = all_events + events["results"]
        offset += limit


def __get_events(base_url, digest_login, offset=0, limit=100):
    """
    Return events.

    :param base_url: The URL to an opencast instance including the tenant
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param offset: The pagination offset
    :type offset: int
    :param limit: The pagination limit
    :type limit: int
    :return: events
    :raise RequestError:
    """

    url = '{}/admin-ng/event/events.json?limit={}&offset={}'.format(base_url, limit, offset)
    response = get_request(url, digest_login, "events")
    json_content = get_json_content(response)

    return json_content
