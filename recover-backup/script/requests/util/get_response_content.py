"""
This module provides methods to decode the response of a rest request to UTF8 and parse the content.
"""

import xml.etree.ElementTree as ElementTree


def get_xml_content(response):
    """
    Decodes the given response to UTF8 and returns it as a json

    :param response:
    :return: response content as xml
    :rtype: ElementTree.Element
    """

    decoded_content = response.content.decode('utf8')
    return ElementTree.fromstring(decoded_content)
