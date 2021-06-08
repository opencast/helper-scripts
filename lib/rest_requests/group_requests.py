from rest_requests.request import post_request


def create_group(base_url, digest_login, name, description="", roles="", users=""):
    """
    Create group.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param name: The name of the group
    :type name: str
    :param description: The description of the group
    :type description: str
    :param roles: The roles of the group
    :type roles: str
    :param users: The users of the group
    :type users: str
    :raise RequestError:
    """
    url = '{}/admin-ng/groups'.format(base_url)
    data = {'name': name, 'description': description, 'roles': roles, 'users': users}
    post_request(url, digest_login, element_description="/admin-ng/groups", data=data)
