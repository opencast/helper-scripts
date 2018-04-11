"""
This module provides methods to decode the response of a rest request to UTF8 and parse the content as either json or xml.
"""

import json
import xml.etree.ElementTree as ET

def get_json_content(response):
    '''
    Decodes the given response to UTF8 and returns it as a json

    :param response:
    :return: resonse content as json
    :rtype: dict
    '''

    decoded_content = response.content.decode('utf8')
    json_content = json.loads(decoded_content)
    return json_content

def get_xml_content(response):
    '''
    Decodes the given response to UTF8 and returns it as a json

    :param response:
    :return: response content as xml
    :rtype: ElementTree.Element
    '''

    decoded_content = response.content.decode('utf8')
    return ET.fromstring(decoded_content)