from rest_requests.request import post_request


def start_workflow(base_url, digest_login, workflow_definition, media_package):
    """
    Starts a workflow on a media package.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param workflow_definition: The workflow definition
    :type workflow_definition: str
    :param media_package: The media package
    :type media_package: str
    :return: The workflow instance
    :rtype: str
    """

    url = '{}/workflow/start'.format(base_url)
    data = {'definition': workflow_definition, 'mediapackage': media_package}

    post_request(url, digest_login, element_description="/workflow/start", data=data)
