from data_handling.errors import SeriesError, optional_mp_error
from rest_requests.series_requests import series_exists
from rest_requests.ingest_media_package import create_media_package, add_track, add_attachment, add_catalog, ingest, \
    add_track_with_url, add_attachment_with_url, add_catalog_with_url
from rest_requests.request_error import RequestError
from import_mp.import_series import import_series


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


def import_mp(series_id, tracks, catalogs, attachments, base_url, digest_login, workflow_id, workflow_config,
              ignore_errors=False, with_url=False):
    """
    Import a media package by first creating a new media package, then adding tracks, catalogs and attachments to it
    and finally ingesting it. Import the series as well if necessary.

    :param series_id: The series id of the mp
    :type series_id: str
    :param tracks: The tracks of the mp
    :type tracks: list
    :param catalogs: The catalogs of the mp
    :type catalogs: list
    :param attachments: The attachments of the mp
    :type attachments: list
    :param base_url: The base url for the rest requests.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param workflow_id: The workflow to be run on ingest.
    :type workflow_id: str
    :param workflow_config: The workflow configuration.
    :type workflow_config: dict
    :param ignore_errors: Whether to ignore errors and import the media package anyway
    :type ignore_errors: bool
    :param with_url: Whether to add the elements via URL
    :type with_url: bool
    :raise MediaPackageError:
    """

    # create empty media package
    new_mp = create_media_package(base_url, digest_login)

    if series_id:

        catalogs, attachments, series_catalogs, series_attachments = \
            __filter_assets(catalogs, attachments)  # series can't have tracks, so don't filter those

        if not series_exists(base_url, digest_login, series_id):

            try:
                import_series(series_id, base_url, digest_login, ignore_errors, series_catalogs, series_attachments)
                print("Imported series {}.".format(series_id))

            except SeriesError as e:
                print("Series {} could not be imported: {}".format(series_id, str(e)))
            except RequestError as e:
                print("Series {} could not be imported: {}".format(series_id, e.error))
            except Exception as e:
                print("Series {} could not be imported: {}".format(series_id, str(e)))

    for track in tracks:
        try:
            if with_url and track.url:
                new_mp = add_track_with_url(base_url, digest_login, new_mp, track)
            else:
                new_mp = add_track(base_url, digest_login, new_mp, track)
        except RequestError as e:
            optional_mp_error("Track {} could not be added.".format(track.id), ignore_errors, e)

    for attachment in attachments:
        try:
            if with_url and attachment.url:
                new_mp = add_attachment_with_url(base_url, digest_login, new_mp, attachment)
            else:
                new_mp = add_attachment(base_url, digest_login, new_mp, attachment)
        except RequestError as e:
            optional_mp_error("Attachment {} could not be added.".format(attachment.id), ignore_errors, e)

    for catalog in catalogs:
        try:
            if with_url and catalog.url:
                new_mp = add_catalog_with_url(base_url, digest_login, new_mp, catalog)
            else:
                new_mp = add_catalog(base_url, digest_login, new_mp, catalog)
        except RequestError as e:
            optional_mp_error("Catalog {} could not be added.".format(catalog.id), ignore_errors, e)

    workflow = ingest(base_url, digest_login, new_mp, workflow_id, workflow_config)
    return workflow
