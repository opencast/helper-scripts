from collections import defaultdict, namedtuple
import xml.etree.ElementTree as ElementTree

import os

from data_handling.errors import MediaPackageError, optional_mp_error

namespaces = {'manifest': 'http://mediapackage.opencastproject.org'}
Element = namedtuple('Element', ['id', 'flavor', 'mimetype', 'filename', 'path', 'tags', 'url'])


def parse_manifest_from_endpoint(manifest, mp_id, ignore_errors=False):
    """
    Parse the media package and collect the media package elements with all relevant information.

    :param manifest: The media package as an xml string
    :type manifest: str
    :param mp_id: The media package id
    :type mp_id: str
    :param ignore_errors: Whether to ignore errors and recover the media package anyway
    :type ignore_errors: bool
    :return: series id, tracks, catalogs, attachments
    :rtype: str, list, list, list
    :raise MediaPackageError:
    """
    try:
        manifest = ElementTree.fromstring(manifest)
    except Exception:
        raise MediaPackageError("Media package {} could not be parsed.".format(mp_id))

    return __parse_manifest(manifest, mp_id, None, ignore_errors)


def parse_manifest_from_filesystem(mp, ignore_errors=False):
    """
    Parse the manifest file and collect the media package elements with all relevant information.

    :param mp: The media package
    :type mp: MediaPackage
    :param ignore_errors: Whether to ignore errors and recover the media package anyway
    :type ignore_errors: bool
    :return: series id, tracks, catalogs, attachments
    :rtype: str, list, list, list
    :raise MediaPackageError:
    """

    manifest_file = os.path.join(mp.path, "manifest.xml")

    if not os.path.isfile(manifest_file):
        raise MediaPackageError("Media package {} is missing it's manifest.".format(mp.id))

    try:
        manifest = ElementTree.parse(manifest_file)
    except Exception:
        raise MediaPackageError("Manifest of media package {} could not be parsed.".format(mp.id))

    return __parse_manifest(manifest, mp.id, mp.path, ignore_errors)


def __parse_manifest(manifest, mp_id, mp_path, ignore_errors=False):
    """
    Parse the manifest and collect the media package elements with all relevant information.

    :param manifest: The media package as an xml Element
    :type manifest: Element
    :param mp_id: The media package id
    :type mp_id: str
    :param mp_path: The path to the media package if it's on a filesystem
    :type mp_path: str or None
    :param ignore_errors: Whether to ignore errors and recover the media package anyway
    :type ignore_errors: bool
    :return: series id, tracks, catalogs, attachments
    :rtype: str, list, list, list
    :raise MediaPackageError:
    """

    series_id = None
    series = manifest.find("./manifest:series", namespaces)
    if series is not None:
        series_id = series.text

    elements = defaultdict(lambda: defaultdict(list))

    for element in ["media", "metadata", "attachments"]:

        for subelement in manifest.findall("./manifest:" + element+"/", namespaces):

            subtype = subelement.tag.split("}")[-1]
            subelement_id = subelement.get("id")

            flavor = subelement.get("type")

            mimetype_element = subelement.find("manifest:mimetype", namespaces)
            mimetype = mimetype_element.text if mimetype_element else None

            url = subelement.find("manifest:url", namespaces).text
            file_extension = url.split(".")[-1]
            if file_extension == "unknown":
                print("File extension for {} {} of media package {} is unknown, falling back to xml.".
                      format(subtype, subelement_id, mp_id))
                file_extension = "xml"

            filename = subelement_id + "." + file_extension
            path = os.path.join(mp_path, filename) if mp_path else None

            if path and not os.path.isfile(path):
                optional_mp_error("{} {} of media package {} cannot be found at {} ."
                                  .format(subtype, subelement_id, mp_id, path), ignore_errors)
                continue

            tag_elements = subelement.findall("manifest:tags/manifest:tag", namespaces)
            tags = None
            if tag_elements:
                tags = [element.text for element in tag_elements]

            elements[element][subtype].append(Element(id=subelement_id, flavor=flavor, mimetype=mimetype,
                                                      filename=filename, path=path, tags=tags, url=url))

    tracks = __get_subtype_elements(elements, "media", "track", mp_id)
    catalogs = __get_subtype_elements(elements, "metadata", "catalog", mp_id)
    attachments = __get_subtype_elements(elements, "attachments", "attachment", mp_id)

    return series_id, tracks, catalogs, attachments


def __get_subtype_elements(elements, element_type, subelement_type, mp_id):
    """
    Get all elements of a specific type and subtype from elements of specific media package, print warnings if there are
    no such elements or if there are elements of a different subtype.

    :param elements: All elements of the specified media package
    :type elements: dict of dicts
    :param element_type: The type of elements to get
    :type element_type: str
    :param subelement_type: The subtype of elements to get
    :type subelement_type: str
    :param mp_id: The ID of the media package
    :type mp_id: str
    :return: All elements with specified type and subtype belonging to the specified media package
    :rtype: list
    """

    if element_type not in elements.keys() or subelement_type not in elements[element_type].keys():
        print("Warning: Media package {} has no {}s.".format(mp_id, subelement_type))
        return []

    if len(elements[element_type].keys()) > 1:
        print("Warning: Media package {} has {} elements that aren't {}s, these will not be recovered."
              .format(mp_id, element_type, subelement_type))

    return elements[element_type][subelement_type]
