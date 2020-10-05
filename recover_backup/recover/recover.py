from data_handling.errors import SeriesError, optional_series_error, optional_mp_error
from data_handling.parse_manifest import parse_manifest_from_filesystem
from data_handling.transform_acl import transform_acl
from input.get_dummy_series_dc import get_dummy_series_dc
from input_output.read_file import read_file
from rest_requests.series_requests import series_exists, create_series
from rest_requests.ingest_media_package import create_media_package, add_track, add_attachment, add_catalog, ingest
from rest_requests.request_error import RequestError


def __filter_assets(catalogs, attachments):
    """
    Separate series from episode assets.

    :param catalogs: All catalogs
    :type: list
    :param attachments: All attachments
    :type attachments: list
    :return: Episode catalogs, episode attachments, series catalogs, series attachments
    :rtype: list, list, list, list
    """
    series_catalogs = [catalog for catalog in catalogs if "series" in catalog.flavor]
    episode_catalogs = [catalog for catalog in catalogs if catalog not in series_catalogs]

    series_attachments = [attachment for attachment in attachments if "series" in attachment.flavor]
    episode_attachments = [attachment for attachment in attachments if attachment not in series_attachments]

    return episode_catalogs, episode_attachments, series_catalogs, series_attachments


def recover_mp(mp, base_url, digest_login, workflow_id, ignore_errors):
    """
    Recover a media package by first creating a new media package, then adding tracks, catalogs and attachments to it
    and finally ingesting it. Recover the series as well if necessary.

    :param mp: The media package to be recovered.
    :type mp: MediaPackage
    :param base_url: The base url for the rest requests.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param workflow_id: The workflow to be run on ingest.
    :type workflow_id: str
    :param ignore_errors: Whether to ignore errors and recover the media package anyway
    :type ignore_errors: bool
    :raise MediaPackageError:
    """

    # create empty media package
    new_mp = create_media_package(base_url, digest_login)

    # parse manifest
    series_id, tracks, catalogs, attachments = parse_manifest_from_filesystem(mp, ignore_errors)

    if series_id:

        catalogs, attachments, series_catalogs, series_attachments = \
            __filter_assets(catalogs, attachments)  # series can't have tracks, so don't filter those

        if not series_exists(base_url, digest_login, series_id):

            try:
                recover_series(series_id, base_url, digest_login, ignore_errors, series_catalogs, series_attachments)
                print("Recovered series {}.".format(series_id))

            except SeriesError as e:
                print("Series {} could not be recovered: {}".format(series_id, str(e)))
            except RequestError as e:
                print("Series {} could not be recovered: {}".format(series_id, e.error))
            except Exception as e:
                print("Series {} could not be recovered: {}".format(series_id, str(e)))

    for track in tracks:
        try:
            new_mp = add_track(base_url, digest_login, new_mp, track)
        except RequestError as e:
            optional_mp_error("Track {} could not be added.".format(track.id), ignore_errors, e)

    for attachment in attachments:
        try:
            new_mp = add_attachment(base_url, digest_login, new_mp, attachment)
        except RequestError as e:
            optional_mp_error("Attachment {} could not be added.".format(attachment.id), ignore_errors, e)

    for catalog in catalogs:
        try:
            new_mp = add_catalog(base_url, digest_login, new_mp, catalog)
        except RequestError as e:
            optional_mp_error("Catalog {} could not be added.".format(catalog.id), ignore_errors, e)

    workflow = ingest(base_url, digest_login, new_mp, workflow_id)
    return workflow


def recover_series(series_id, base_url, digest_login, ignore_errors, series_catalogs, series_attachments=None):
    """
    Recover a series by recreating it with the series Dublin Core catalog and optionally a series ACL.

    :param series_id: The ID of the series
    :type series_id: str
    :param base_url: The base url for the rest requests.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param ignore_errors: Whether to ignore errors and recover the media package anyway
    :type ignore_errors: bool
    :param series_catalogs: The series catalogs
    :type series_catalogs: list
    :param series_attachments: The series attachments (optional)
    :type series_attachments: list or None
    :raise SeriesError:
    """

    series_dcs = [catalog for catalog in series_catalogs if catalog.flavor == "dublincore/series"]
    series_acls = [attachment for attachment in series_attachments if attachment.flavor == "security/xacml+series"]

    if len(series_dcs) > 1 or len(series_acls) > 1:
        optional_series_error("More than one series Dublin Core catalog or ACL in series {}.".format(series_id),
                              ignore_errors)

    if not series_dcs:
        optional_series_error("Series Dublin Core catalog of series {} missing.".format(series_id), ignore_errors)

    series_dc_contents = []
    series_acl_contents = []

    for series_dc in series_dcs:
        try:
            series_dc_content = read_file(series_dc.path)
            series_dc_contents.append(series_dc_content)
        except Exception as e:
            optional_series_error("Series Dublin Core catalog of series {} could not be read.".format(series_id),
                                  ignore_errors, e)

    for series_acl in series_acls:
        try:
            series_acl_content = read_file(series_acl.path)
        except Exception as e:
            optional_series_error("Series ACL of series {} could not be read.".format(series_id), ignore_errors, e)
            continue

        try:
            series_acl_content = transform_acl(series_acl_content)
            series_acl_contents.append(series_acl_content)
        except Exception as e:
            optional_series_error("Series ACL of series {} could not be transformed.".format(series_id), ignore_errors,
                                  e)

    series_dc_content = series_dc_contents[0] if series_dc_contents else get_dummy_series_dc(series_id)
    series_acl_content = series_acl_contents[0] if series_acl_contents else None

    create_series(base_url, digest_login, series_dc_content, series_acl_content)
