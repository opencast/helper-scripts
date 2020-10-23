from collections import defaultdict, namedtuple
import xml.etree.ElementTree as ElementTree

import os

from data_handling.errors import MediaPackageError, optional_mp_error

namespaces = {'manifest': 'http://mediapackage.opencastproject.org'}

Asset = namedtuple('Asset', ['id', 'flavor', 'mimetype', 'filename', 'path', 'tags', 'url'])
Publication = namedtuple('Publication', ['channel', 'tracks', 'attachments', 'catalogs'])
MediaPackage = namedtuple('MediaPackage', ['id', 'series_id', 'tracks', 'attachments', 'catalogs', 'publications'])


def parse_manifest_from_endpoint(manifest, mp_id, ignore_errors=False, with_publications=False):
    """
    Parse the media package and collect the media package elements with all relevant information.

    :param manifest: The media package as an xml string
    :type manifest: str
    :param mp_id: The media package id
    :type mp_id: str
    :param ignore_errors: Whether to ignore errors and recover the media package anyway
    :type ignore_errors: bool
    :param with_publications: Whether to include publication elements
    :type with_publications: bool
    :return: The MediaPackage
    :rtype: MediaPackage
    :raise MediaPackageError:
    """
    try:
        manifest = ElementTree.fromstring(manifest)
    except Exception:
        raise MediaPackageError("Media package {} could not be parsed.".format(mp_id))

    return __parse_manifest(manifest, mp_id, None, ignore_errors, with_publications)


def parse_manifest_from_filesystem(mp, ignore_errors=False, with_publications=False):
    """
    Parse the manifest file and collect the media package elements with all relevant information.

    :param mp: The media package
    :type mp: Snapshot
    :param ignore_errors: Whether to ignore errors and recover the media package anyway
    :type ignore_errors: bool
    :param with_publications: Whether to include publication elements
    :type with_publications: bool
    :return: The MediaPackage
    :rtype: MediaPackage
    :raise MediaPackageError:
    """

    manifest_file = os.path.join(mp.path, "manifest.xml")

    if not os.path.isfile(manifest_file):
        raise MediaPackageError("Media package {} is missing it's manifest.".format(mp.id))

    try:
        manifest = ElementTree.parse(manifest_file)
    except Exception:
        raise MediaPackageError("Manifest of media package {} could not be parsed.".format(mp.id))

    return __parse_manifest(manifest, mp.id, mp.path, ignore_errors, with_publications)


def __parse_manifest(manifest, mp_id, mp_path, ignore_errors=False, with_publications=False):
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
    :param with_publications: Whether to include publication elements
    :type with_publications: bool
    :return: The MediaPackage
    :rtype: MediaPackage
    :raise MediaPackageError:
    """

    series_id = None
    series = manifest.find("./manifest:series", namespaces)
    if series is not None:
        series_id = series.text

    tracks, catalogs, attachments = _get_assets(manifest, mp_id, mp_path, ignore_errors)
    publications = None

    if with_publications:
        publications = []
        for publication in manifest.findall("./manifest:publications/", namespaces):
            channel = publication.get("channel")
            pub_tracks, pub_catalogs, pub_attachments = _get_assets(publication, mp_id, mp_path, ignore_errors, False)
            publications.append(Publication(channel=channel, tracks=pub_tracks, attachments=pub_attachments,
                                            catalogs=pub_catalogs))

    return MediaPackage(id=mp_id, series_id=series_id, tracks=tracks, attachments=attachments, catalogs=catalogs,
                        publications=publications)


def _get_assets(target, mp_id, mp_path, ignore_errors, warn=True):

    elements = defaultdict(lambda: defaultdict(list))

    for element in ["media", "metadata", "attachments"]:

        for sub_element in target.findall("./manifest:" + element+"/", namespaces):

            subtype = sub_element.tag.split("}")[-1]
            sub_element_id = sub_element.get("id")

            flavor = sub_element.get("type")

            mimetype_element = sub_element.find("manifest:mimetype", namespaces)
            mimetype = mimetype_element.text if (mimetype_element is not None) else None

            url = sub_element.find("manifest:url", namespaces).text
            file_extension = url.split(".")[-1]
            if file_extension == "unknown":
                print("File extension for {} {} of media package {} is unknown, falling back to xml.".
                      format(subtype, sub_element_id, mp_id))
                file_extension = "xml"

            filename = sub_element_id + "." + file_extension
            path = os.path.join(mp_path, filename) if mp_path else None

            if path and not os.path.isfile(path):
                optional_mp_error("{} {} of media package {} cannot be found at {} ."
                                  .format(subtype, sub_element_id, mp_id, path), ignore_errors)
                continue

            tag_elements = sub_element.findall("manifest:tags/manifest:tag", namespaces)
            tags = None
            if tag_elements:
                tags = [element.text for element in tag_elements]

            elements[element][subtype].append(Asset(id=sub_element_id, flavor=flavor, mimetype=mimetype,
                                                    filename=filename, path=path, tags=tags, url=url))

    tracks = __get_subtype_elements(elements, "media", "track", mp_id, warn)
    catalogs = __get_subtype_elements(elements, "metadata", "catalog", mp_id, warn)
    attachments = __get_subtype_elements(elements, "attachments", "attachment", mp_id, warn)

    return tracks, catalogs, attachments


def __get_subtype_elements(elements, element_type, sub_element_type, mp_id, warn=True):
    """
    Get all elements of a specific type and subtype from elements of specific media package, print warnings if there are
    no such elements or if there are elements of a different subtype.

    :param elements: All elements of the specified media package
    :type elements: dict of dicts
    :param element_type: The type of elements to get
    :type element_type: str
    :param sub_element_type: The subtype of elements to get
    :type sub_element_type: str
    :param mp_id: The ID of the media package
    :type mp_id: str
    :return: All elements with specified type and subtype belonging to the specified media package
    :rtype: list
    """

    if warn:
        if element_type not in elements.keys() or sub_element_type not in elements[element_type].keys():
            print("Warning: Media package {} has no {}s.".format(mp_id, sub_element_type))
            return []

        if len(elements[element_type].keys()) > 1:
            print("Warning: Media package {} has {} elements that aren't {}s, these will not be processed."
                  .format(mp_id, element_type, sub_element_type))

    return elements[element_type][sub_element_type]
