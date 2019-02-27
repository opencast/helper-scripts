"""
This module contains methods to get ACLs or Dublin Core catalogs of a series or event from the rest api.
"""
from data_handling.elements import get_id
from data_handling.types import ElementDescription, AssetTypeDescription, AssetDescription
from rest_requests.get_response_content import get_xml_content, get_json_content
from rest_requests.request import get_request


def __get_dc_of_series(series, base_url, digest_login):
    """
    Get the series Dublin Core catalog for a given series.

    :param series: The series
    :type series: dict
    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login delete_artefacts for digest authentication
    :type digest_login: DigestLogin
    :return: The series Dublin Core catalog
    :rtype: ElementTree.Element
    :raise RequestError:
    """

    url = '{}/series/{}.xml'.format(base_url, get_id(series))

    es = ElementDescription.SERIES
    es = es.unknown()

    response = get_request(url, digest_login, es, AssetTypeDescription.SERIES.singular(),
                           AssetDescription.DC.singular())

    series_dc = get_xml_content(response)

    return series_dc


def __get_acl_of_series(series, base_url, digest_login):
    """
    Get the series ACL for a given series.

    :param series: The series
    :type series: dict
    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login delete_artefacts for digest authentication
    :type digest_login: DigestLogin
    :return: The series ACL
    :rtype: dict
    :raise RequestError:
    """

    url = "{}/series/{}/acl.json".format(base_url, get_id(series))

    response = get_request(url, digest_login, ElementDescription.SERIES.unknown(),
                           AssetTypeDescription.SERIES.singular(),
                           AssetDescription.ACL.singular())

    json_content = get_json_content(response)

    series_acl = json_content["acl"]

    return series_acl


def __get_acls_of_event(event, base_url, digest_login):
    """
    Get two lists for episode and series ACLs for a given event.

    :param event: The event
    :type event: dict
    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login delete_artefacts for digest authentication
    :type digest_login: DigestLogin
    :return: The episode and series acls
    :rtype: list, list
    :raise RequestError:
    """

    url = '{}/admin-ng/event/{}/asset/attachment/attachments.json'.format(base_url, get_id(event))

    response = get_request(url, digest_login, ElementDescription.EVENT.unknown(), AssetTypeDescription.BOTH.plural(),
                           AssetDescription.ACL.plural())

    json_content = get_json_content(response)

    episode_acls = [__get_asset_content(acl, digest_login, ElementDescription.EVENT.unknown(),
                                        AssetTypeDescription.EPISODE.singular(), AssetDescription.ACL.singular())
                    for acl in json_content if "security-policy-episode" in acl["id"]]
    series_acls = [__get_asset_content(acl, digest_login, ElementDescription.EVENT.unknown(),
                                       AssetTypeDescription.SERIES.singular(), AssetDescription.ACL.singular())
                   for acl in json_content if "security-policy-series" in acl["id"]]

    return episode_acls, series_acls


def __get_dcs_of_event(event, base_url, digest_login):
    """
    Get two lists for episode and series Dublin Core catalogs for a given event.

    :param event: The event
    :type event: dict
    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login delete_artefacts for digest authentication
    :type digest_login: DigestLogin
    :return: The episode and series Dublin Core catalogs
    :rtype: list, list
    :raise RequestError:
    """

    url = '{}/admin-ng/event/{}/asset/catalog/catalogs.json'.format(base_url, get_id(event))

    response = get_request(url, digest_login, ElementDescription.EVENT.unknown(), AssetTypeDescription.BOTH.plural(),
                           AssetDescription.DC.plural())

    json_content = get_json_content(response)

    episode_dcs = [__get_asset_content(catalog, digest_login, ElementDescription.EVENT.unknown(),
                                       AssetTypeDescription.EPISODE.singular(), AssetDescription.DC.singular())
                   for catalog in json_content if "dublincore/episode" in catalog["type"]]
    series_dcs = [__get_asset_content(catalog, digest_login, ElementDescription.EVENT.unknown(),
                                      AssetTypeDescription.SERIES.singular(), AssetDescription.DC.singular())
                  for catalog in json_content if "dublincore/series" in catalog["type"]]

    return episode_dcs, series_dcs


def __get_asset_content(asset, digest_login, element_description, asset_type_description, asset_description):
    """
    Use URL of server response to get the actual content of the asset.

    :param asset: The asset information
    :type asset: dict
    :param digest_login: The login delete_artefacts for digest authentication
    :type digest_login: DigestLogin
    :param asset_description: ACL or Dublin Core catalog
    :type asset_description: str
    :return: The actual asset content in xml format
    :rtype: ElementTree.Element
    :raise RequestError:
    """

    url = asset["url"]

    response = get_request(url, digest_login, element_description, asset_type_description, asset_description)

    dc = get_xml_content(response)

    return dc


def get_asset_of_series_from_rest(series, base_url, digest_login, asset_description):
    """
    Get the series asset for a given series.

    :param series: The series
    :type series: dict
    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login delete_artefacts for digest authentication
    :type digest_login: DigestLogin
    :param asset_description: DC or ACL
    :type asset_description: AssetDescription
    :return: The series asset
    :rtype: ElementTree.Element
    :raise RequestError:
    """

    if asset_description == AssetDescription.DC:
        return __get_dc_of_series(series, base_url, digest_login)
    else:
        return __get_acl_of_series(series, base_url, digest_login)


def get_assets_of_event_from_rest(event, base_url, digest_login, asset_description):
    """
    Get two lists of episode and series assets for a given event depending on the given asset description.

    :param event: The event
    :type event: dict
    :param base_url: The base URL for the request
    :type base_url: str
    :param digest_login: The login delete_artefacts for digest authentication
    :type digest_login: DigestLogin
    :param asset_description: DC or ACL
    :type asset_description: AssetDescription
    :return: The episode and series assets
    :rtype: list, list
    :raise RequestError:
    """

    if asset_description == AssetDescription.DC:
        return __get_dcs_of_event(event, base_url, digest_login)
    else:
        return __get_acls_of_event(event, base_url, digest_login)
