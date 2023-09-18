import json

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


def start_task(base_url, digest_login, workflow_definition, event_id):
    """
    Start a workflow on a media package.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param workflow_definition: The workflow definition
    :type workflow_definition: str
    :param event_id: the event id
    :type event_id: str
    :return: The workflow instance id
    :rtype: int
    :raise RequestError:
    """

    url = '{}/admin-ng/tasks/new'.format(base_url)
    # hardcode workflow definition and ingest start date since I don't think it's actually relevant
    metadata = {'workflow': workflow_definition,
                'configuration': {'{}'.format(event_id): {"workflowDefinitionId": "fast",
                                                          "ingest_start_date": "20210607T020914Z"}}}
    data = {'metadata': json.dumps(metadata)}

    response = post_request(url, digest_login, element_description="/admin-ng/tasks/new", data=data)
    workflow_instance_id = get_json_content(response)[0]
    return workflow_instance_id


def get_workflow_instance(base_url, digest_login, id):
    """
    Get workflow instance.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param id: The workflow instance id
    :type id: int
    :return: the workflow instance
    :rtype: dict
    """

    url = '{}/workflow/instance/{}.json'.format(base_url, id)

    response = get_request(url, digest_login, "workflow instance")
    return get_json_content(response)["workflow"]


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


def get_list_of_workflow_instances(base_url, digest_login, params):
    """
    Wrapper for get_workflow_instances() to get only a list of workflow instances, not the additional information.

    :param base_url: The URL for the request
    :type base_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param params: Additional parameters
    :type params: dict
    :return: list of workflow instances
    :rtype: list
    """

    workflows = get_workflow_instances(base_url, digest_login, params)

    if "workflow" not in workflows:
        return []

    workflows = workflows["workflow"]
    if not isinstance(workflows, list):  # happens if there's only one
        workflows = [workflows]
    return workflows
