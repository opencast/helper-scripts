"""
This module provides methods to get event assets from an oaipmh record that is in the matterhorn-inlined format.
"""

from check_data.types import AssetType
from data_handling.namespaces import namespaces


def __get_dcs_from_oaipmh(record):
    """
    Get all dublincore catalogs from an oaipmh record.

    :param record:
    :type record: ElementTree.Element
    :return: episode dublincores, series dublincores
    :rtype: list, list
    """

    dcs = record.findall(".//inlined:catalog", namespaces)

    episode_dcs = [dc.find("dc:dublincore", namespaces) for dc in dcs if dc.get('type') == 'dublincore/episode']
    series_dcs = [dc.find("dc:dublincore", namespaces) for dc in dcs if dc.get('type') == 'dublincore/series']

    return episode_dcs, series_dcs

def __get_acls_from_oaipmh(record):
    """
    Get all ACLs from an oaipmh record.

    :param record:
    :type record: ElementTree.Element
    :return: episode ACLs, series ACLs
    :rtype: list, list
    """

    acls = record.findall(".//inlined:attachment", namespaces)

    episode_acls = [acl.find("acl:Policy", namespaces) for acl in acls if acl.get('type') == 'security/xacml+episode']
    series_acls = [acl.find("acl:Policy", namespaces) for acl in acls if acl.get('type') == 'security/xacml+series']

    return episode_acls, series_acls

def get_assets_from_oaipmh(record, assettype):
    """
    Get all assets of the specified type from an oaipmh record.

    :param record:
    :type record: ElementTree.Element
    :param assettype:
    :type assettype: str
    :return: list, list
    """

    if assettype == AssetType.DC:
        return __get_dcs_from_oaipmh(record)
    else:
        return __get_acls_from_oaipmh(record)