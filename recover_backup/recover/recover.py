from data_handling.errors import SeriesError
from data_handling.parse_manifest import parse_manifest
from data_handling.transform_acl import transform_acl
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


def recover_mp(mp, base_url, digest_login, workflow_id):
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
    :raise MediaPackageError:
    """

    new_mp = create_media_package(base_url, digest_login)

    series_id, tracks, catalogs, attachments = parse_manifest(mp)

    if series_id:

        catalogs, attachments, series_catalogs, series_attachments = \
            __filter_assets(catalogs, attachments)  # series can't have tracks, so don't filter those

        if not series_exists(base_url, digest_login, series_id):

            try:
                recover_series(base_url, digest_login, series_catalogs, series_attachments)
                print("Recovered series {}.".format(series_id))

            except SeriesError as e:
                print("Series {} could not be recovered: {}".format(series_id, str(e)))
            except RequestError as e:
                print("Series {} could not be recovered: {}".format(series_id, e.error))
            except Exception as e:
                print("Series {} could not be recovered: {}".format(series_id, str(e)))

    for track in tracks:

        new_mp = add_track(base_url, digest_login, new_mp, track)

    for attachment in attachments:

        new_mp = add_attachment(base_url, digest_login, new_mp, attachment)

    for catalog in catalogs:

        new_mp = add_catalog(base_url, digest_login, new_mp, catalog)

    workflow = ingest(base_url, digest_login, new_mp, workflow_id)
    return workflow


def recover_series(base_url, digest_login, series_catalogs, series_attachments=None):
    """
    Recover a series by recreating it with the series Dublin Core catalog and optionally a series ACL.

    :param base_url: The base url for the rest requests.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param series_catalogs: The series catalogs
    :type series_catalogs: list
    :param series_attachments: The series attachments (optional)
    :type series_attachments: list or None
    :raise: SeriesError
    """

    series_dc = [catalog for catalog in series_catalogs if catalog.flavor == "dublincore/series"]
    series_acl = [attachment for attachment in series_attachments if attachment.flavor == "security/xacml+series"]

    if len(series_dc) > 1 or len(series_acl) > 1:
        raise SeriesError("More than one series Dublin Core catalog or ACL, recovery of series not possible.")

    if not series_dc:
        raise SeriesError("Series Dublin Core catalog missing, recovery of series not possible.")

    series_dc = series_dc[0]
    series_acl = series_acl[0] if series_acl else None

    series_dc_content = read_file(series_dc.path)
    series_acl_content = read_file(series_acl.path) if series_acl else None

    series_acl_content = transform_acl(series_acl_content)

    create_series(base_url, digest_login, series_dc_content, series_acl_content)
