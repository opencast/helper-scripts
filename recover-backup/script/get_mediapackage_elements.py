from collections import defaultdict, namedtuple
import xml.etree.ElementTree as ElementTree

import os

namespaces = {'manifest': 'http://mediapackage.opencastproject.org'}
Element = namedtuple('Element', ['id', 'flavor', 'mimetype', 'filename', 'path', 'tags'])


class MediapackageError(Exception):
    """
    Represents all errors that can hinder the recovery of a mediapackage.
    Simply contains an error message and nothing else.
    """
    pass


def get_mediapackage_elements(mp):
    """
    Parse the manifest file and collect the media package elements with all relevant information.

    :param mp: The given mediapackage.
    :type mp: MediaPackage
    :return: List of mediapackage elements.
    :rtype: Element
    """

    manifest_file = os.path.join(mp.path, "manifest.xml")

    if not os.path.isfile(manifest_file):
        raise MediapackageError("Mediapackage {} is missing it's manifest.".format(mp.id))

    try:
        manifest = ElementTree.parse(manifest_file)
    except Exception:
        raise MediapackageError("Manifest of mediapackage {} could not be parsed.".format(mp.id))

    elements = defaultdict(lambda: defaultdict(list))

    for element in ["media", "metadata", "attachments"]:

        for subelement in manifest.findall("./manifest:" + element+"/", namespaces):

            subtype = subelement.tag.split("}")[-1]

            subelement_id = subelement.get("id")
            flavor = subelement.get("type")
            mimetype = subelement.find("manifest:mimetype", namespaces).text
            file_extension = subelement.find("manifest:url", namespaces).text.split(".")[-1]
            filename = subelement_id + "." + file_extension
            path = os.path.join(mp.path, filename)

            tag_elements = subelement.findall("manifest:tags/manifest:tag", namespaces)
            tags = None

            if tag_elements:
                tags = [element.text for element in tag_elements]

            if not os.path.isfile(path):
                raise MediapackageError("Mediapackage {} is missing a {} with id {}.".format(mp.id, subtype,
                                                                                             subelement_id))

            elements[element][subtype].append(Element(id=subelement_id, flavor=flavor, mimetype=mimetype,
                                                      filename=filename, path=path, tags=tags))

    tracks = __get_subtype_elements(elements, "media", "track", mp.id)
    catalogs = __get_subtype_elements(elements, "metadata", "catalog", mp.id)
    attachments = __get_subtype_elements(elements, "attachments", "attachment", mp.id)

    return tracks, catalogs, attachments


def __get_subtype_elements(elements, element_type, subelement_type, mp_id):

    if element_type not in elements.keys() or subelement_type not in elements[element_type].keys():
        print("Warning: Mediapackage {} has no {}s.".format(mp_id, subelement_type))
        return None

    if len(elements[element_type].keys()) > 1:
        print("Warning: Mediapackage {} has {} elements that aren't {}s, these will not be recovered."
              .format(mp_id, element_type, subelement_type))

    return elements[element_type][subelement_type]
