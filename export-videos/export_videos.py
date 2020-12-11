import os

from data_handling.flavor_matcher import matches_flavor
from rest_requests.file_requests import get_video_file
from rest_requests.stream_security_requests import sign_url


def export_videos(mp, mp_dir, server_url, digest_login, export_archived, export_publications, export_mimetypes,
                  export_flavors, sign=False):
    """
    Request the tracks of the media package that meet the criteria and export them to video files.

    :param mp: The media package whose tracks should be exported
    :type mp: MediaPackage
    :param mp_dir: The directory for the media package
    :type mp_dir: Path
    :param export_archived: Whether to export archived tracks
    :type export_archived: bool
    :param export_publications: The publications to be exported
    :type export_publications: list
    :param export_mimetypes: The mimetypes to be exported
    :type export_mimetypes: list
    :param export_flavors: The flavors to be exported
    :type export_flavors: list
    :param server_url: The server URL
    :type server_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param sign: Whether to sign the URL first
    :type sign: bool
    """

    # check archived tracks
    if export_archived:
        target_dir = os.path.join(mp_dir, 'archived')

        for track in mp.tracks:
            if __check_track(track, export_mimetypes, export_flavors):
                try:
                    __export_track(target_dir, track, server_url, digest_login, sign)
                except Exception as e:
                    print("Archived Track {} of media package {} could not be exported: {}"
                          .format(track.id, mp.id, str(e)))

    # check published tracks
    if export_publications:
        for publication in mp.publications:
            if publication.channel in export_publications:
                target_dir = os.path.join(mp_dir, publication.channel)

                for track in publication.tracks:
                    if __check_track(track, export_mimetypes, export_flavors):
                        try:
                            __export_track(target_dir, track, server_url, digest_login, sign)
                        except Exception as e:
                            print("Track {} of publication {} of media package {} could not be exported: {}"
                                  .format(track.id, publication.channel, mp.id, str(e)))


def __check_track(track, export_mimetypes, export_flavors):
    """
    Check if track meets criteria for export.

    :param track: The track to be checked
    :type track: Asset
    :param export_mimetypes: The mimetypes to be exported
    :type export_mimetypes: list
    :param export_flavors: The flavors to be exported
    :type export_flavors: list
    :return: If the track should be exported.
    :rtype: bool
    """
    return (not export_mimetypes or track.mimetype in export_mimetypes) and \
           (not export_flavors or matches_flavor(track.flavor, export_flavors))


def __export_track(target_dir, track, server_url, digest_login, sign=False):
    """
    Request a video and write it to a file. Sign the URL first if necessary.

    :param target_dir: The directory to put the video file in
    :type target_dir: Path
    :param track: The track to be exported
    :type track: Asset
    :param server_url: The server URL
    :type server_url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param sign: Whether to sign the URL first
    :type sign: bool
    :raise: RequestError
    """

    url = track.url

    file_extension = url.split(".")[-1]
    filename = '{}.{}'.format(track.id, file_extension)
    path = os.path.join(target_dir, filename)

    if sign:
        url = sign_url(digest_login, server_url, url)

    os.makedirs(target_dir, exist_ok=True)

    get_video_file(digest_login, url, path)
