from check_data.types import ElementType
from data_handling.element_util import get_id
from rest_requests.get_request import __get_request
from rest_requests.get_response_content import get_xml_content


def get_oaipmh_publications(event):

    return [(publication["id"], publication["url"]) for publication in event["publications"]
            if "oaipmh" in publication["id"]]


def get_oaipmh_record(event, repository_url, repository, digest_login, base_url):
    """
    Gets oaipmh record for a given event with the given base_url and digest login.

    :param event:
    :type event: dict
    :param repository_url:
    :type repository_url: str
    :param repository: OAIPMH repository id
    :type repository: str
    :param digest_login:
    :type digest_login: DigestLogin
    :param base_url:
    :type base_url: str
    :return: oaipmh record
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

    response = __get_request(url, digest_login, ElementType.OAIPMH.singular.format(repository))

    record = get_xml_content(response)

    return record
