from rest_requests.get_response_content import get_json_content
from rest_requests.request import post_request, get_request, delete_request, put_request


def create_group(base_url, digest_login, group):
    """
    Create group.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param group: The group to create
    :type group: dict
    :raise RequestError:
    """
    url = '{}/api/groups'.format(base_url)
    post_request(url, digest_login, element_description="/api/groups", data=group)


def update_group(base_url, digest_login, group):
    """
    Update group.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param group: The group to create
    :type group: dict
    :raise RequestError:
    """
    url = '{}/api/groups/{}'.format(base_url, group["identifier"])
    put_request(url, digest_login, element_description="/api/groups", data=group)


def delete_group(base_url, digest_login, group_id):
    """
    Delete group.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param group_id: The id of the group to delete
    :type group_id: str
    :raise RequestError:
    """
    url = '{}/api/groups/{}'.format(base_url, group_id)
    delete_request(url, digest_login, "/api/groups/<id>")


def get_all_groups(base_url, digest_login):
    """
    Get all groups.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :return: groups
    :rtype: list
    :raise RequestError:
    """
    url = '{}/api/groups'.format(base_url)
    groups = get_json_content(get_request(url, digest_login, "/api/groups"))
    return groups
