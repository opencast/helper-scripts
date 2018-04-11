"""
This module provides functionality to compare assets (ACLs and dublincore catalogs).
"""

def compare_dc(dc1, dc2):
    """
    Compares two dublincore catalogs by comparing the tag and text of every child.

    :param dc1:
    :type dc1: ElementTree.Element
    :param dc2:
    :type dc2: ElementTree.Element
    :return: true if equal
    :rtype: bool
    """

    if not dc1 and not dc2:
        return True

    if (not dc1 and dc2) or (dc1 and not dc2):
        return False

    children1 = dc1.findall("*")
    children2 = dc2.findall("*")

    if len(children1) != len(children2):
        return False

    for child1, child2 in zip(children1, children2):

        tag1 = child1.tag
        tag2 = child2.tag

        if tag1 != tag2:
            return False

        text1 = child1.text
        text2 = child2.text

        if text1 != text2:
            return False

    return True

def compare_acl(acl1, acl2):
    """
    Compares two ACLs by comparing the role, action and allow setting for every ACE.

    :param acl1:
    :type acl1: dict with role, action as key and allow as value
    :param acl2:
    :type acl2: dict with role, action as key and allow as value
    :return: true if equal
    :rtype: bool
    """

    if not acl1 and not acl2:
        return True

    if (not acl1 and acl2) or (acl1 and not acl2):
        return False

    keys1 = acl1.keys()
    keys2 = acl2.keys()

    if len(keys1) != len(keys2):
        return False

    for key in keys1:

        if key not in keys2:
            return False

        if acl1[key] != acl2[key]:
            return False

    return True