from rest_requests.get_response_content import get_json_content
from rest_requests.request import get_request


def get_events_of_series(base_url, digest_login, series_id):
    """
    Get the events for a series from the API

    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param series_id: The series id
    :type series_id: str
    :return: list of events
    :rtype: list
    :raise RequestError:
    """

    url = '{}/api/events/?filter=is_part_of:{}'.format(base_url, series_id)

    response = get_request(url, digest_login, "events")
    return get_json_content(response)
