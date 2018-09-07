"""
This module provides methods to make some basic requests to the opencast REST API.
"""

from shared.rest_requests.request import get_request
from shared.rest_requests.get_response_content import get_json_content

JAVA_MAX_INT = 2147483647


def get_tenants(base_url, digest_login):
    """
    Return a sorted list of unique tenant IDs

    :param base_url: The URL to an opencast instance
    :type base_url: str
    :param digest_login: The login data for digest authentication
    :type digest_login: DigestLogin
    :return: tenant ids
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
    :param digest_login: The login data for digest authentication
    :type digest_login: DigestLogin
    :return: series
    """

    url = '{}/admin-ng/series/series.json?limit={}'.format(base_url, JAVA_MAX_INT)

    response = get_request(url, digest_login, "series")

    json_content = get_json_content(response)

    return json_content["results"]


def get_events(base_url, digest_login):
    """
    Return all events of one tenant.

    :param base_url: The URL to an opencast instance including the tenant
    :type base_url: str
    :param digest_login: The login data for digest authentication
    :type digest_login: DigestLogin
    :return: events
    """

    url = '{}/admin-ng/event/events.json?limit={}'.format(base_url, JAVA_MAX_INT)

    response = get_request(url, digest_login, "events")

    json_content = get_json_content(response)

    return json_content["results"]
