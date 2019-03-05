from data_handling.elements import get_id
from data_handling.types import ElementDescription
from rest_requests.get_response_content import get_xml_content
from rest_requests.request import get_request


def get_oaipmh_record(event, repository_url, repository, digest_login, base_url):
    """
    Get the oaipmh record for a given event at base_url with the given digest login.

    :param event: The event
    :type event: dict
    :param repository_url: The URL to the OAIPMH repository
    :type repository_url: str
    :param repository: The OAIPMH repository ID
    :type repository: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param base_url: The URL of the opencast instance
    :type base_url: str
    :return: The OAIPMH record in XML format
    :rtype: ElementTree.Element
    """

    # absolute url
    if repository_url.startswith("http"):

        url = '{}?verb=GetRecord&metadataPrefix=matterhorn-inlined&identifier={}'.format(repository_url.split('?')[0],
                                                                                         get_id(event))
    # relative url
    else:
        url = '{}{}?verb=GetRecord&metadataPrefix=matterhorn-inlined&identifier={}'.format(base_url,
                                                                                           repository_url.split('?')[0],
                                                                                           get_id(event))

    response = get_request(url, digest_login, ElementDescription.OAIPMH.format(repository).singular())

    record = get_xml_content(response)

    return record
