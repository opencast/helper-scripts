"""
This module provides methods to decode the response of a rest request to UTF8 and parse the content in different
formats.
"""

import json
import xml.etree.ElementTree as ElementTree


def get_json_content(response):
    """
    Decodes the given response to UTF8 and returns it in JSON

    :param response: The response to a request
    :return: The response content as json
    :rtype: dict
    """

    decoded_content = response.content.decode('utf8')
    json_content = json.loads(decoded_content)
    return json_content


def get_xml_content(response):
    """
    Decodes the given response to UTF8 and returns it in XML

    :param response: The response to a request
    :return: The response content as xml
    :rtype: ElementTree.Element
    """

    decoded_content = response.content.decode('utf8')

    return ElementTree.fromstring(decoded_content)


def get_string_content(response):
    """
    Decodes the given response to UTF8 and returns it as a string

    :param response: The response to a request
    :return: resonse content as string
    :rtype: dict
    """

    decoded_content = response.content.decode('utf8')
    return decoded_content
