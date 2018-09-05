from xml.etree import ElementTree


namespaces = {'acl': 'urn:oasis:names:tc:xacml:2.0:policy:schema:os', 'root': 'ns0'}


def transform_acl(xacml):
    """
    Transform an XACML into the shorter xml format so that the series service understands them.

    :param xacml: The XACML
    :type xacml: str
    :return: More minimal ACL in XML format
    :rtype: str
    """

    xacml = ElementTree.fromstring(xacml)

    xml_declaration = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

    root_element = ElementTree.Element("acl")
    root_element.set('xmlns', namespaces['acl'])

    rules = xacml.findall(".//acl:Rule", namespaces)

    for rule in rules:

        rule_id = rule.get("RuleId")
        if rule_id == "DenyRule":
            continue  # skip global deny rule

        effect = rule.get("Effect")

        action = rule.find(".//acl:ActionMatch//acl:AttributeValue", namespaces).text
        role = rule.find(".//acl:Condition/acl:Apply/acl:AttributeValue", namespaces).text
        allow = (effect == "Permit")

        ace_element = ElementTree.SubElement(root_element, "ace")

        action_element = ElementTree.SubElement(ace_element, "action")
        action_element.text = action

        allow_element = ElementTree.SubElement(ace_element, "allow")
        allow_element.text = str(allow).lower()

        role_element = ElementTree.SubElement(ace_element, "role")
        role_element.text = role

    new_xml = xml_declaration + ElementTree.tostring(root_element, encoding="unicode")
    return new_xml
