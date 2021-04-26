from rest_requests.get_response_content import get_json_content
from rest_requests.request import get_request


def get_episode_from_search(base_url, digest_login, event_id):
    """
    Get episode from search as json.

    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param event_id: The event id
    :type event_id: str
    :return: episode as json or None
    :rtype: episode as json or None
    :raise RequestError:
    """

    url = '{}/search/episode.json?id={}'.format(base_url, event_id)

    response = get_request(url, digest_login, "search episode")
    search_results = get_json_content(response)["search-results"]
    if "result" in search_results:
        return search_results["result"]
    return None
