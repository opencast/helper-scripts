"""
This module provides methods to parse ACLs in json and xml format into another format so they can be easily compared.
"""

from xml.etree import ElementTree

from shared.data.namespaces import namespaces


def parse_acl(acl):
    """
    Parses an ACL in json or xml format into a dict.

    :param acl: The ACL
    :type acl: ElementTree.Element or dict
    :return: dict with (role, action) as key and allow as value
    :rtype: dict
    """

    if isinstance(acl, ElementTree.Element):
        return parse_xml_acl(acl)
    else:
        return parse_json_acl(acl)


def parse_xml_acl(xml_acl):
    """
    Parses an ACL in xml format into a dict.

    :param xml_acl: The ACL in xml format
    :type xml_acl: ElementTree.Element
    :return: dict with (role, action) as key and allow as value
    :rtype: dict
    """

    acl = {}

    rules = xml_acl.findall(".//acl:Rule", namespaces)

    for rule in rules:

        rule_id = rule.get("RuleId")
        if rule_id == "DenyRule":
            continue  # skip global deny rule

        effect = rule.get("Effect")

        action = rule.find(".//acl:ActionMatch//acl:AttributeValue", namespaces).text
        role = rule.find(".//acl:Condition/acl:Apply/acl:AttributeValue", namespaces).text
        allow = (effect == "Permit")

        acl[(role, action)] = allow

    return acl


def parse_json_acl(json_acl):
    """
    Parses an ACL in json format into a dict.

    :param json_acl: The ACL in json format
    :type json_acl: dict
    :return: dict with (role, action) as key and allow as value
    :rtype: dict
    """

    acl = {}

    for ace in json_acl["ace"]:
        role = ace["role"]
        action = ace["action"]
        allow = ace["allow"]

        acl[(role, action)] = allow

    return acl
