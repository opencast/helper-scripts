import os
import sys

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

import config
from input_output.unique_names import make_dirname_unique
from args.digest_login import DigestLogin
from data_handling.elements import get_id
from data_handling.parse_manifest import parse_manifest_from_endpoint
from export import export_videos, export_catalogs
from parse_args import parse_args
from rest_requests.api_requests import get_events_of_series
from rest_requests.assetmanager_requests import get_media_package
from rest_requests.search_requests import get_episode_from_search


def main():
    """
    Export video files
    """

    event_ids, series_ids = parse_args()
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)

    if not hasattr(config, 'presentation_url') or not config.presentation_url:
        config.presentation_url = config.admin_url

    # get events from all series
    if series_ids:
        print("Getting events for series.")
        events = []
        for series_id in series_ids:
            try:
                events_of_series = get_events_of_series(config.admin_url, digest_login, series_id)
                events += events_of_series
            except Exception as e:
                print("Events of series {} could not be requested: {}".format(series_id, str(e)))

        if not events:
            __abort_script("No events found.")

        event_ids = [get_id(event) for event in events]

    print("Starting export process.")
    series_dirs = {}
    for event_id in event_ids:
        try:
            print("Exporting media package {}".format(event_id))

            # get mp from search
            search_mp = None
            if config.export_search:
                search_mp_json = get_episode_from_search(config.presentation_url, digest_login, event_id)
                if search_mp_json:
                    search_mp_xml = search_mp_json["ocMediapackage"]
                    search_mp = parse_manifest_from_endpoint(search_mp_xml, event_id, False, False)

            # get mp from archive
            archive_mp_xml = get_media_package(config.admin_url, digest_login, event_id)
            archive_mp = parse_manifest_from_endpoint(archive_mp_xml, event_id, False, True)

            # build target directory path
            target_dir = config.target_directory
            if config.create_series_dirs and archive_mp.series_id:
                if config.title_folders:
                    # if we use series titles as folder names, we need to remember the directory so we don't create a
                    # new one for the same series
                    if archive_mp.series_id in series_dirs:
                        series_dir = series_dirs[archive_mp.series_id]
                    else:
                        series_dir = make_dirname_unique(target_dir, archive_mp.series_title)
                        series_dirs[archive_mp.series_id] = series_dir
                else:
                    series_dir = archive_mp.series_id
                target_dir = os.path.join(target_dir, series_dir)

            mp_dir = make_dirname_unique(target_dir, archive_mp.title) if config.title_folders else archive_mp.id
            target_dir = os.path.join(target_dir, mp_dir)

            # export
            export_videos(archive_mp, search_mp, target_dir, config.admin_url, digest_login, config.export_archived,
                          config.export_publications, config.export_mimetypes, config.export_flavors,
                          config.stream_security, config.original_filenames)

            if config.export_catalogs:
                export_catalogs(archive_mp, target_dir, config.admin_url, digest_login, config.export_catalogs,
                                config.stream_security, config.original_filenames)

        except Exception as e:
            print("Tracks of media package {} could not be exported: {}".format(event_id, str(e)))

    print("Done.")


def __abort_script(message):
    """
    Print message and abort script.
    :param message: The error message
    :type message: str
    """
    print(message)
    sys.exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
