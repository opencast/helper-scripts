from rest_requests.get_request import __get_request
from rest_requests.get_response_content import get_json_content

JAVA_MAX_INT = 2147483647

def get_tenants(base_url, digest_login):
    """
    Returns a sorted list of unique tenant ids

    :param base_url:
    :type base_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :return: tenant ids
    """

    url = '{}/org/all.json'.format(base_url)

    response = __get_request(url, digest_login, "tenants")

    json_content = get_json_content(response)

    if isinstance(json_content["organizations"]["organization"], list):
        tenants = [org["id"] for org in (json_content["organizations"])["organization"]]
        tenants = sorted(set(tenants))
    else:
        tenants = [json_content["organizations"]["organization"]["id"]]
    return tenants

def get_series(base_url, digest_login):
    """
    Returns all series of one tenant.

    :param base_url:
    :type base_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :return: series
    """

    url = '{}/admin-ng/series/series.json?limit={}'.format(base_url, JAVA_MAX_INT)

    response = __get_request(url, digest_login, "series")

    json_content = get_json_content(response)

    return json_content["results"]

def get_events(base_url, digest_login):
    """
    Returns all events of one tenant.

    :param base_url:
    :type base_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :return: events
    """

    url = '{}/admin-ng/event/events.json?limit={}'.format(base_url, JAVA_MAX_INT)

    response = __get_request(url, digest_login, "events")

    json_content = get_json_content(response)

    return json_content["results"]