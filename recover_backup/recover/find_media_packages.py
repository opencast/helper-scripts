""" This module finds the media packages in the backup that are to be recovered."""

from collections import namedtuple
import os
from operator import attrgetter

from input_output.input import get_number

MediaPackage = namedtuple('MediaPackage', ["id", "version", "path"])


def find_media_packages(backup_path, tenant, use_last_version, media_package_ids=None):
    """
    Find the media packages to be recovered in the directory given by the backup path, the tenant and the respective id,
    ask for the version to be recovered or use the last version.

    :param media_package_ids: IDs of the media packages that are to be recovered
    :type media_package_ids: list
    :param backup_path: Path to backup of archive directory
    :type backup_path: str
    :param tenant: Tenant ID
    :type tenant: str
    :param use_last_version: Whether to always recover the last version of a media package
    :type use_last_version: bool
    :return: List of media packages to be recovered containing their ids, the chosen version and path to the version
    directory
    :rtype: list
    """

    tenant_dir = os.path.abspath(os.path.join(backup_path, tenant))

    if not os.path.isdir(tenant_dir):
        print("Directory for tenant {} at path {} could not be found.".format(tenant, tenant_dir))
        return

    if not media_package_ids:

        dir_name, sub_dirs, files = next(os.walk(tenant_dir))
        media_package_ids = [subdir for subdir in sub_dirs]

    media_package_ids = sorted(media_package_ids)

    mps_to_recover = []

    for mp_id in media_package_ids:

        mp_dir = os.path.abspath(os.path.join(tenant_dir, mp_id))

        if not os.path.isdir(mp_dir):
            print("Directory for media package {} at path {} could not be found, skipped.".format(mp_id, mp_dir))
            continue

        dir_name, sub_dirs, files = next(os.walk(mp_dir))

        if not sub_dirs:
            print("Media package {} at path {} does not contain any snapshots, skipped.".format(mp_id, mp_dir))
            continue

        snapshots = []
        for subdir in sub_dirs:
            try:
                snapshot = int(subdir)
                snapshots.append(snapshot)
            except ValueError:
                pass

        if len(snapshots) == 0:
            print("Media package {} at path {} does not contain any snapshots, skipped.".format(mp_id, mp_dir))
            continue

        snapshots.sort()

        # choose version
        if use_last_version or len(snapshots) == 1:
            version = snapshots[-1]

        else:

            prompt = "Choose version for media package {} from {}: ".format(mp_id, ", ".join(map(str, snapshots)))
            invalid = "This version is not available for media package {}.".format(mp_id)
            version = get_number(prompt, invalid, snapshots)

        version_dir = os.path.join(mp_dir, str(version))

        mps_to_recover.append(MediaPackage(id=mp_id, version=version, path=version_dir))

    return sorted(mps_to_recover, key=attrgetter('id'))
