"""
This module provides methods to get assets from an oaipmh record in the matterhorn-inlined format.
"""
from data_handling.namespaces import namespaces
from data_handling.types import AssetDescription


def __get_dcs_from_oaipmh(record):
    """
    Get all Dublin Core catalogs from an oaipmh record.

    :param record: The OAIPMH record
    :type record: ElementTree.Element
    :return: episode Dublin Core catalogs, series Dublin Core catalogs
    :rtype: list, list
    """

    dcs = record.findall(".//inlined:catalog", namespaces)

    episode_dcs = [dc.find("dc:dublincore", namespaces) for dc in dcs if dc.get('type') == 'dublincore/episode']
    series_dcs = [dc.find("dc:dublincore", namespaces) for dc in dcs if dc.get('type') == 'dublincore/series']

    return episode_dcs, series_dcs


def __get_acls_from_oaipmh(record):
    """
    Get all ACLs from an oaipmh record.

    :param record: The OAIPMH record
    :type record: ElementTree.Element
    :return: episode ACLs, series ACLs
    :rtype: list, list
    """

    acls = record.findall(".//inlined:attachment", namespaces)

    episode_acls = [acl.find("acl:Policy", namespaces) for acl in acls if acl.get('type') == 'security/xacml+episode']
    series_acls = [acl.find("acl:Policy", namespaces) for acl in acls if acl.get('type') == 'security/xacml+series']

    return episode_acls, series_acls


def get_assets_from_oaipmh(record, asset_description):
    """
    Get all assets of the specified type from an oaipmh record.

    :param record: The OAIPMH record
    :type record: ElementTree.Element
    :param asset_description: ACLs or Dublin Core catalogs
    :type asset_description: AssetDescription
    :return: Two lists with episode and series assets
    :rtype: list, list
    """

    if asset_description == AssetDescription.DC:
        return __get_dcs_from_oaipmh(record)
    else:
        return __get_acls_from_oaipmh(record)
