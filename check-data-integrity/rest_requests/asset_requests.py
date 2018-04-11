"""
This module contains methods to get ACLs or dublincore catalogs of a series or event from the rest api.
"""

from check_data.types import AssetType
from data_handling.element_util import get_id
from rest_requests.get_request import __get_request
from rest_requests.get_response_content import get_json_content, get_xml_content
    
def __get_dc_of_series(series, base_url, digest_login):
    """
    Returns the series dublincore catalog for a given series.

    :param series:
    :type series: dict
    :param base_url:
    :type base_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :return: series dublincore catalog
    :rtype: ElementTree.Element
    :raise: RequestError
    """

    url = '{}/series/{}.xml'.format(base_url, get_id(series))

    response = __get_request(url, digest_login, "dublincore catalog of series")

    series_dc = get_xml_content(response)

    return series_dc

def __get_acl_of_series(series, base_url, digest_login):
    """
    Returns the series ACL for a given series.

    :param series:
    :type series: dict
    :param base_url:
    :type base_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :return: series ACL
    :rtype: dict
    :raise: RequestError
    """

    url = "{}/series/{}/acl.json".format(base_url, get_id(series))

    response = __get_request(url, digest_login, "acl of series")

    json_content = get_json_content(response)

    series_acl = json_content["acl"]

    return series_acl

def __get_acls_of_event(event, base_url, digest_login):
    """
    Returns two lists of episode and series ACLs for a given event.

    :param event:
    :type event: dict
    :param base_url:
    :type base_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :return: episode acls, series acls
    :rtype: list, list
    :raise: RequestError
    """

    url = '{}/admin-ng/event/{}/asset/attachment/attachments.json'.format(base_url, get_id(event))

    response = __get_request(url, digest_login, "acls of event")

    json_content = get_json_content(response)

    episode_acls = [__get_asset_as_xml(catalog, digest_login, "episode acl of event") for catalog in json_content if "security-policy-episode" in catalog["id"]]
    series_acls = [__get_asset_as_xml(catalog, digest_login, "series acl of event") for catalog in json_content if "security-policy-series" in catalog["id"]]

    return episode_acls, series_acls

def __get_dcs_of_event(event, base_url, digest_login):
    """
    Returns two lists of episode and series dublincore catalogs for a given event.

    :param event:
    :type event: dict
    :param base_url:
    :type base_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :return: episode dublincores, series dublincores
    :rtype: list, list
    :raise: RequestError
    """

    url = '{}/admin-ng/event/{}/asset/catalog/catalogs.json'.format(base_url, get_id(event))

    response = __get_request(url, digest_login, "dublincore catalogs of event")

    json_content = get_json_content(response)

    episode_dcs = [__get_asset_as_xml(catalog, digest_login, "episode dublincore of event") for catalog in json_content if "dublincore/episode" in catalog["type"]]
    series_dcs = [__get_asset_as_xml(catalog, digest_login, "series dublincore of event") for catalog in json_content if "dublincore/series" in catalog["type"]]

    return episode_dcs, series_dcs

def __get_asset_as_xml(asset, digest_login, asset_description):
    """
    Use URL of server response to get the actual asset.

    :param asset:
    :type asset: dict
    :param digest_login:
    :type digest_login: DigestLogin
    :param asset_description:
    :type asset_description: str
    :return: asset in xml format
    :rtype: ElementTree.Element
    :raise: RequestError
    """

    url = asset["url"]

    response = __get_request(url, digest_login, asset_description)

    dc = get_xml_content(response)

    return dc


def get_asset_of_series_from_rest(series, base_url, digest_login, asset_type):
    '''
    Returns the series asset for a given series.

    :param series:
    :type series: dict
    :param base_url:
    :type base_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :param asset_type: DC or ACL
    :type asset_type: AssetType
    :return: series asset
    :rtype: ElementTree.Element
    :raise: RequestError
    '''

    if asset_type == AssetType.DC:
        return __get_dc_of_series(series, base_url, digest_login)
    else:
        return __get_acl_of_series(series, base_url, digest_login)


def get_assets_of_event_from_rest(event, base_url, digest_login, asset_type):
    """
    Returns two lists of episode and series assets for a given event depending on the given assettype.

    :param event:
    :type event: dict
    :param base_url:
    :type base_url: str
    :param digest_login:
    :type digest_login: DigestLogin
    :return: episode assets, series assets
    :param asset_type: DC or ACL
    :type asset_type: AssetType
    :rtype: list, list
    :raise: RequestError
    """

    if asset_type == AssetType.DC:
        return __get_dcs_of_event(event, base_url, digest_login)
    else:
        return __get_acls_of_event(event, base_url, digest_login)