from collections import defaultdict, namedtuple
import xml.etree.ElementTree as ET

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
        manifest = ET.parse(manifest_file)
    except Exception:
        raise MediapackageError("Manifest of mediapackage {} could not be parsed.".format(mp.id))

    elements = defaultdict(lambda: defaultdict(list))

    for element in ["media", "metadata", "attachments"]:

        for medium in manifest.findall("./manifest:" + element+"/", namespaces):

            subtype = medium.tag.split("}")[-1]

            id = medium.get("id")
            flavor = medium.get("type")
            mimetype = medium.find("manifest:mimetype", namespaces).text
            file_extension = medium.find("manifest:url", namespaces).text.split(".")[-1]
            filename = id + "." + file_extension
            path = os.path.join(mp.path, filename)

            tag_elements = medium.findall("manifest:tags/manifest:tag", namespaces)
            tags = None

            if tag_elements:
                tags = [element.text for element in tag_elements]

            if not os.path.isfile(path):
                raise MediapackageError("Mediapackage {} is missing a {} with id {}.".format(mp.id, subtype, id))

            elements[element][subtype].append(Element(id=id, flavor=flavor, mimetype=mimetype, filename=filename,
                                                      path=path, tags=tags))

    tracks = __get_subtype_elements(elements, "media", "track", mp.id)
    catalogs = __get_subtype_elements(elements, "metadata", "catalog", mp.id)
    attachments = __get_subtype_elements(elements, "attachments", "attachment", mp.id)

    return tracks, catalogs, attachments

def __get_subtype_elements(elements, type, subtype, mp_id):

    if not type in elements.keys() or not subtype in elements[type].keys():
        print("Warning: Mediapackage {} has no {}s.".format(mp_id, subtype))
        return None

    if len(elements[type].keys()) > 1:
        print("Warning: Mediapackage {} has {} elements that aren't {}s, these will not be recovered.".format(mp_id, type, subtype))

    return elements[type][subtype]