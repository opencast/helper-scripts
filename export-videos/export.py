import os

from data_handling.flavor_matcher import matches_flavor
from input_output.unique_names import make_filename_unique
from rest_requests.file_requests import export_video_file, export_text_file
from rest_requests.stream_security_requests import sign_url, accepts_url


def export_videos(archive_mp, search_mp, mp_dir, server_url, digest_login, export_archived, export_publications,
                  export_mimetypes, export_flavors, sign, original_filenames):
    """
    Request the tracks of the media package that meet the criteria and export them to video files.

    :param archive_mp: The media package whose tracks should be exported
    :type archive_mp: MediaPackage
    :param search_mp: The search media package whose tracks should be exported (optional)
    :type search_mp: MediaPackage
    :param mp_dir: The directory for the media package
    :type mp_dir: Path
    :param server_url: The server URL
    :type server_url: str
    :param export_archived: Whether to export archived tracks
    :type export_archived: bool
    :param export_publications: The publications to be exported
    :type export_publications: list
    :param export_mimetypes: The mimetypes to be exported
    :type export_mimetypes: list
    :param export_flavors: The flavors to be exported
    :type export_flavors: list
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param sign: Whether to sign the URL first
    :type sign: bool
    :param original_filenames: Whether to keep the original filenames on export (otherwise track id is used)
    :type original_filenames: bool
    """

    # check archived tracks
    if export_archived:
        target_dir = os.path.join(mp_dir, 'archived')
        __export_tracks(archive_mp.id, archive_mp.tracks, target_dir, server_url, digest_login, export_mimetypes,
                        export_flavors, sign, original_filenames)

    # check published tracks
    if export_publications:
        for publication in archive_mp.publications:
            if publication.channel in export_publications:
                target_dir = os.path.join(mp_dir, publication.channel)
                __export_tracks(archive_mp.id, publication.tracks, target_dir, server_url, digest_login,
                                export_mimetypes, export_flavors, sign, original_filenames, publication.channel)

    # check search service
    if search_mp:
        target_dir = os.path.join(mp_dir, 'search')
        __export_tracks(search_mp.id, search_mp.tracks, target_dir, server_url, digest_login, export_mimetypes,
                        export_flavors, sign, original_filenames, 'search')


def __export_tracks(mp_id, tracks, target_dir, server_url, digest_login, export_mimetypes, export_flavors, sign,
                    original_filenames, publication_channel=None):
    """
    Export tracks.

    :param mp_id: Media package id
    :type mp_id: str
    :param tracks: The tracks
    :type tracks: list
    :param target_dir: The target directory
    :type target_dir: Path
    :param server_url: The server URL
    :type server_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param export_mimetypes: The mimetypes to be exported
    :type export_mimetypes: list
    :param export_flavors: The flavors to be exported
    :type export_flavors: list
    :param sign: Whether to sign the URL first
    :type sign: bool
    :param original_filenames: Whether to keep the original filenames on export (otherwise track id is used)
    :type original_filenames: bool
    :param publication_channel: The publication channel (for logging only)
    :type publication_channel: str
    """

    for track in tracks:
        if __check_if_export(track, export_mimetypes, export_flavors):
            try:
                __export(target_dir, track, server_url, digest_login, sign, original_filenames)
            except Exception as e:
                if publication_channel:
                    print("Track {} of publication '{}' of media package {} could not be exported: {}"
                          .format(track.id, publication_channel, mp_id, str(e)))
                else:
                    print("Track {} of media package {} could not be exported: {}".format(track.id, mp_id, str(e)))


def export_catalogs(archive_mp, mp_dir, server_url, digest_login, export_flavors, sign, original_filenames):
    """
    Request the catalogs of the media package that meet the criteria and export them to files.

    :param archive_mp: The media package whose catalogs should be exported
    :type archive_mp: MediaPackage
    :param mp_dir: The directory for the media package
    :type mp_dir: Path
    :param export_flavors: The flavors to be exported
    :type export_flavors: list
    :param server_url: The server URL
    :type server_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param sign: Whether to sign the URL first
    :type sign: bool
    :param original_filenames: Whether to keep the original filenames on export (otherwise catalog id is used)
    :type original_filenames: bool
    """

    target_dir = os.path.join(mp_dir, 'catalogs')
    __export_catalogs(archive_mp.id, archive_mp.catalogs, target_dir, server_url, digest_login, export_flavors, sign,
                      original_filenames)


def __export_catalogs(mp_id, catalogs, target_dir, server_url, digest_login, export_flavors, sign, original_filenames):
    """
    Export catalogs.

    :param mp_id: Media package id
    :type mp_id: str
    :param catalogs: The catalogs
    :type catalogs: list
    :param target_dir: The target directory
    :type target_dir: Path
    :param server_url: The server URL
    :type server_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param export_flavors: The flavors to be exported
    :type export_flavors: list
    :param sign: Whether to sign the URL first
    :type sign: bool
    :param original_filenames: Whether to keep the original filenames on export (otherwise catalog id is used)
    :type original_filenames: bool
    """

    for catalog in catalogs:
        if __check_if_export(catalog, [], export_flavors):  # mimetypes not supported for catalogs yet
            try:
                __export(target_dir, catalog, server_url, digest_login, sign, original_filenames, is_video=False)
            except Exception as e:
                print("Catalog {} of media package {} could not be exported: {}".format(catalog.id, mp_id, str(e)))


def __check_if_export(asset, export_mimetypes, export_flavors):
    """
    Check if asset meets criteria for export.

    :param asset: The asset to be checked
    :type asset: Asset
    :param export_mimetypes: The mimetypes to be exported
    :type export_mimetypes: list
    :param export_flavors: The flavors to be exported
    :type export_flavors: list
    :return: If the asset should be exported.
    :rtype: bool
    """
    return (not export_mimetypes or asset.mimetype in export_mimetypes) and \
           (not export_flavors or matches_flavor(asset.flavor, export_flavors))


def __export(target_dir, asset, server_url, digest_login, sign, original_filenames, is_video=True):
    """
    Request an asset and write it to a file. Sign the URL first if necessary.

    :param target_dir: The directory to put the video file in
    :type target_dir: Path
    :param asset: The asset to be exported
    :type asset: Asset
    :param server_url: The server URL
    :type server_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param sign: Whether to sign the URL first
    :type sign: bool
    :param original_filenames: Whether to keep the original filename (otherwise asset id is used)
    :type original_filenames: bool
    :param is_video: Whether the requested file is a video (default: true)
    :type is_video: bool
    :raise: RequestError
    """

    url = asset.url

    file_extension = url.split(".")[-1]
    if original_filenames:
        filename = os.path.basename(url).replace("." + file_extension, '')
        filename = make_filename_unique(target_dir, filename, file_extension)
    else:
        filename = asset.id
    path = os.path.join(target_dir, '{}.{}'.format(filename, file_extension))

    if sign:
        if accepts_url(digest_login, server_url, url):
            url = sign_url(digest_login, server_url, url)

    os.makedirs(target_dir, exist_ok=True)

    if is_video:
        export_video_file(digest_login, url, path)
    else:
        export_text_file(digest_login, url, path)
