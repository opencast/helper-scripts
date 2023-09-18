from rest_requests.get_response_content import get_json_content
from rest_requests.request import get_request, delete_request, NOT_FOUND
from rest_requests.request_error import RequestError


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


def get_failed_events(base_url, digest_login):
    """
    Get failed events from the API

    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :return: list of events
    :rtype: list
    :raise RequestError:
    """

    url = '{}/api/events/?filter=status:EVENTS.EVENTS.STATUS.PROCESSING_FAILURE'.format(base_url)
    response = get_request(url, digest_login, "failed events")
    return get_json_content(response)


def get_event(base_url, digest_login, event_id):
    """
    Get event.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param event_id: The id of the event to delete
    :type event_id: str
    :raise RequestError:
    """
    url = '{}/api/events/{}'.format(base_url, event_id)
    response = get_request(url, digest_login, "/api/events/<id>")
    return get_json_content(response)


def event_exists(base_url, digest_login, event_id):
    """
    Check if an event exists.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param event_id: The id of the event
    :type event_id: str
    :return: true if it exists, false otherwise
    :rtype: bool
    :raise RequestError:
    """

    try:
        get_event(base_url, digest_login, event_id)
    except RequestError as e:
        if e.has_status_code() and e.get_status_code() == NOT_FOUND:
            return False
        raise e
    return True


def delete_event(base_url, digest_login, event_id):
    """
    Delete event.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param event_id: The id of the event to delete
    :type event_id: str
    :raise RequestError:
    """
    url = '{}/api/events/{}'.format(base_url, event_id)
    delete_request(url, digest_login, "/api/events/<id>")
