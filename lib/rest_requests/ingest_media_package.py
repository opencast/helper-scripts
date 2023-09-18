from collections import namedtuple

from rest_requests.get_response_content import get_xml_content
from rest_requests.request import get_request, post_request, big_post_request, put_request

Workflow = namedtuple("Workflow", ["id", "template", "mp_id"])


def create_media_package(base_url, digest_login):
    """
    Create a new media package represented by an XML string.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :return: New media package.
    :rtype: str
    :raise RequestError:
    """

    url = '{}/ingest/createMediaPackage'.format(base_url)

    response = get_request(url, digest_login, "/ingest/createMediaPackage")
    return response.content.decode('utf8')


def create_media_package_with_id(base_url, digest_login, mp_id):
    """
    Create a new media package represented by an XML string with the given identifier.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp_id: The media package id to use
    :type mp_id: str
    :return: New media package.
    :rtype: str
    :raise RequestError:
    """

    url = '{}/ingest/createMediaPackageWithID/{}'.format(base_url, mp_id)

    response = put_request(url, digest_login, "/ingest/createMediaPackageWithID")
    return response.content.decode('utf8')


def add_attachment(base_url, digest_login, mp, attachment):
    """
    Add an attachment to a new media package.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New media package.
    :type mp: str
    :param attachment: The attachment to be added.
    :type attachment: Asset
    :return: Augmented media package.
    :rtype: str
    :raise RequestError:
    """

    url = '{}/ingest/addAttachment'.format(base_url)
    data = {'flavor': attachment.flavor, 'mediaPackage': mp}
    files = {'BODY': open(attachment.path, 'rb')}

    response = post_request(url, digest_login, "/ingest/addAttachment", data=data, files=files)
    return response.content


def add_attachment_with_url(base_url, digest_login, mp, attachment):
    """
    Add an attachment to a new media package via URL.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New media package.
    :type mp: str
    :param attachment: The attachment to be added.
    :type attachment: Asset
    :return: Augmented media package.
    :rtype: str
    :raise RequestError:
    """

    url = '{}/ingest/addAttachment'.format(base_url)
    data = {'flavor': attachment.flavor, 'mediaPackage': mp, 'url': attachment.url, 'tags': ','.join(attachment.tags)}

    response = post_request(url, digest_login, "/ingest/addAttachment", data=data)
    return response.content


def add_catalog(base_url, digest_login, mp, catalog):
    """
    Add a catalog to a new media package.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New media package.
    :type mp: str
    :param catalog: The catalog to be added.
    :type catalog: Asset
    :return: Augmented media package.
    :rtype: str
    :raise RequestError:
    """

    url = '{}/ingest/addCatalog'.format(base_url)
    data = {'flavor': catalog.flavor, 'mediaPackage': mp}
    files = {'BODY': open(catalog.path, 'rb')}

    response = post_request(url, digest_login, "/ingest/addCatalog", data=data, files=files)
    return response.content


def add_catalog_with_url(base_url, digest_login, mp, catalog):
    """
    Add a catalog to a new media package via URL.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New media package.
    :type mp: str
    :param catalog: The catalog to be added.
    :type catalog: Asset
    :return: Augmented media package.
    :rtype: str
    :raise RequestError:
    """

    url = '{}/ingest/addCatalog'.format(base_url)
    data = {'flavor': catalog.flavor, 'mediaPackage': mp, 'url': catalog.url, 'tags': ','.join(catalog.tags)}

    response = post_request(url, digest_login, "/ingest/addCatalog", data=data)
    return response.content


def add_track(base_url, digest_login, mp, track):
    """
    Add a track to a new media package.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New media package.
    :type mp: str
    :param track: The catalog to be added.
    :type track: Asset
    :return: Augmented media package.
    :rtype: str
    :raise RequestError:
    """

    url = '{}/ingest/addTrack'.format(base_url)
    data = {'flavor': track.flavor, 'mediaPackage': mp}

    response = big_post_request(url, digest_login, "/ingest/addTrack", data=data, files=[track.path])
    return response.content


def add_track_with_url(base_url, digest_login, mp, track):
    """
    Add a track to a new media package via URL.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New media package.
    :type mp: str
    :param track: The track to be added.
    :type track: Asset
    :return: Augmented media package.
    :rtype: str
    :raise RequestError:
    """

    url = '{}/ingest/addTrack'.format(base_url)
    data = {'flavor': track.flavor, 'mediaPackage': mp, 'url': track.url, 'tags': ','.join(track.tags)}

    response = post_request(url, digest_login, "/ingest/addTrack", data=data)
    return response.content


def ingest(base_url, digest_login, mp, workflow_id, workflow_config):
    """
    Ingest media package and start a workflow.

    :param base_url: Base URL for request.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param mp: New media package.
    :type mp: str
    :param workflow_id: The workflow to be run on ingest.
    :type workflow_id: str
    :param workflow_config: The workflow configuration.
    :type workflow_config: dict
    :return: Information about the started workflow.
    :rtype: Workflow
    :raise RequestError:
    """

    if workflow_id:
        url = '{}/ingest/ingest/{}'.format(base_url, workflow_id)
    else:
        url = '{}/ingest/ingest/'.format(base_url)

    data = {'mediaPackage': mp}
    data.update(workflow_config)  # add workflow parameters

    response = post_request(url, digest_login, "/ingest/ingest", data=data)
    return __parse_ingest_response(response)


def schedule(base_url, digest_login, mp, workflow_id, workflow_config, ca_config, start_date, end_date):

    if workflow_id:
        url = '{}/ingest/schedule/{}'.format(base_url, workflow_id)
    else:
        url = '{}/ingest/schedule/'.format(base_url)

    data = {'mediaPackage': mp, 'start': start_date, 'end': end_date}
    data.update(workflow_config)  # add workflow parameters
    data.update(ca_config)  # add capture agent parameters

    post_request(url, digest_login, "/ingest/schedule", data=data)


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
    media_package = workflow.find("mp:mediapackage", namespaces)
    mp_id = media_package.get("id")

    return Workflow(id=workflow_id, template=workflow_template, mp_id=mp_id)


def add_assets(base_url, digest_login, new_mp, attachments, catalogs, tracks):
    for catalog in catalogs:
        new_mp = add_catalog_with_url(base_url, digest_login, new_mp, catalog)

    for attachment in attachments:
        new_mp = add_attachment_with_url(base_url, digest_login, new_mp, attachment)

    for track in tracks:
        new_mp = add_track_with_url(base_url, digest_login, new_mp, track)
    return new_mp
