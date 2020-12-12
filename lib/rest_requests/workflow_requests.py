from rest_requests.get_response_content import get_json_content
from rest_requests.request import post_request, get_request


def start_workflow(base_url, digest_login, workflow_definition, media_package):
    """
    Start a workflow on a media package.

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
    :raise RequestError:
    """

    url = '{}/workflow/start'.format(base_url)
    data = {'definition': workflow_definition, 'mediapackage': media_package}

    post_request(url, digest_login, element_description="/workflow/start", data=data)


def get_workflow_instances(base_url, digest_login, params):
    """
    Get workflow instances.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param params: Additional parameters
    :type params: dict
    :return: list of workflow instances
    :rtype: dict
    """

    url = '{}/workflow/instances.json'.format(base_url)

    for i, param in enumerate(params):
        if i == 0:
            url += "?"
        else:
            url += "&"
        url += param + "=" + params.get(param)

    response = get_request(url, digest_login, "workflow instances")
    return get_json_content(response)["workflows"]
