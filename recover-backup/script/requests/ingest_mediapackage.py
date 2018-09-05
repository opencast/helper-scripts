from collections import namedtuple

from script.requests.util.get_response_content import get_xml_content
from script.requests.util.request import post_request, get_request

Workflow = namedtuple("Workflow", ["id", "template", "mp_id"])


def create_mediapackage(base_url, digest_login):
    """
    Create a new mediapackage represented by an XML string.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :return: New mediapackage.
    :rtype: str
    """

    url = '{}/ingest/createMediaPackage'.format(base_url)

    response = get_request(url, digest_login, "/ingest/createMediapackage")

    return response.content.decode('utf8')


def add_attachment(base_url, digest_login, mp, attachment):
    """
    Add an attachment to a new mediapackage.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New mediapackage.
    :type mp: str
    :param attachment: The attachment to be added.
    :type attachment: Element
    :return: Augmented mediapackage.
    :rtype: str
    """

    url = '{}/ingest/addAttachment'.format(base_url)

    data = {'flavor': attachment.flavor, 'mediaPackage': mp}
    files = {'BODY': open(attachment.path, 'rb')}

    response = post_request(url, digest_login, "/ingest/addAttachment", data, files)

    return response.content


def add_catalog(base_url, digest_login, mp, catalog):
    """
    Add a catalog to a new mediapackage.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New mediapackage.
    :type mp: str
    :param catalog: The catalog to be added.
    :type catalog: Element
    :return: Augmented mediapackage.
    :rtype: str
    """

    url = '{}/ingest/addCatalog'.format(base_url)

    data = {'flavor': catalog.flavor, 'mediaPackage': mp}
    files = {'BODY': open(catalog.path, 'rb')}

    response = post_request(url, digest_login, "/ingest/addCatalog", data, files)

    return response.content


def add_track(base_url, digest_login, mp, track):
    """
    Add a track to a new mediapackage.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New mediapackage.
    :type mp: str
    :param track: The catalog to be added.
    :type track: Element
    :return: Augmented mediapackage.
    :rtype: str
    """

    url = '{}/ingest/addTrack'.format(base_url)

    data = {'flavor': track.flavor, 'mediaPackage': mp}
    files = {'BODY': open(track.path, 'rb')}

    response = post_request(url, digest_login, "/ingest/addTrack", data, files)

    return response.content


def ingest(base_url, digest_login, mp, workflow_id):
    """
    Ingest mediapackage and start a workflow.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New mediapackage.
    :type mp: str
    :param workflow_id: The workflow to be run on ingest.
    :type workflow_id: str
    :return: Information about the started workflow.
    :rtype: Workflow
    """

    if workflow_id:

        url = '{}/ingest/ingest/{}'.format(base_url, workflow_id)
    else:
        url = '{}/ingest/ingest/'.format(base_url)

    data = {'mediaPackage': mp}

    response = post_request(url, digest_login, "/ingest/ingest", data, None)
    return __parse_ingest_response(response)


def __parse_ingest_response(response):
    """
    Parse relevant information from the response of /ingest.

    :param response:
    :return: Information about the started workflow.
    :rtype: Workflow
    """

    namespaces = {"mp": "http://mediapackage.opencastproject.org", "wf": "http://workflow.opencastproject.org"}

    workflow = get_xml_content(response)
    workflow_id = workflow.get("id")
    workflow_template = workflow.find("wf:template", namespaces).text
    mediapackage = workflow.find("mp:mediapackage", namespaces)
    mp_id = mediapackage.get("id")

    return Workflow(id=workflow_id, template=workflow_template, mp_id=mp_id)
