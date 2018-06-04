""" This module finds the mediapackages in the backup that are to be recovered."""

from collections import namedtuple
import os
from operator import attrgetter

from script.input.util.input import get_number

MediaPackage = namedtuple('MediaPackage', ["id", "version", "path"])


def find_all_mediapackages(backup_path, tenant, use_last_version):
    """
    Find all mediapackages in the directory given by the backup path and the tenant for recovery, ask for the version
    to be recovered or use the last version.

    :param backup_path: Path to backup of archive directory
    :type backup_path: str
    :param tenant: Tenant ID
    :type tenant: str
    :param use_last_version: Whether to always recover the last version of a mediapackage
    :type use_last_version: bool
    :return: List of mediapackages to be recovered containing their ids, the chosen version and path to the version
    directory
    :rtype: list
    """

    tenant_dir = os.path.abspath(os.path.join(backup_path, tenant))
    dir_name, subdirs, files = next(os.walk(tenant_dir))

    mediapackage_ids = [subdir for subdir in subdirs]

    return find_mediapackages(mediapackage_ids, backup_path, tenant, use_last_version)


def find_mediapackages(mediapackage_ids, backup_path, tenant, use_last_version):
    """
    Find the mediapackages to be recovered in the directory given by the backup path, the tenant and the respective id,
    ask for the version to be recovered or use the last version.

    :param mediapackage_ids: IDs of the mediapackages that are to be recovered
    :type mediapackage_ids: list
    :param backup_path: Path to backup of archive directory
    :type backup_path: str
    :param tenant: Tenant ID
    :type tenant: str
    :param use_last_version: Whether to always recover the last version of a mediapackage
    :type use_last_version: bool
    :return: List of mediapackages to be recovered containing their ids, the chosen version and path to the version
    directory
    :rtype: list
    """

    mediapackage_ids = sorted(mediapackage_ids)

    mps_to_recover = []

    for mp_id in mediapackage_ids:

        mp_dir = os.path.abspath(os.path.join(backup_path, tenant, mp_id))

        if not os.path.isdir(mp_dir):
            print("Directory for mediapackage {} at path {} could not be found, skipped".format(mp_id, mp_dir))
            continue

        dir_name, subdirs, files = next(os.walk(mp_dir))

        if not subdirs:
            print("Mediapackage {} at path {} does not contain any snapshots, skipped".format(mp_id, mp_dir))
            continue

        snapshots = []
        for subdir in subdirs:
            try:
                snapshot = int(subdir)
                snapshots.append(snapshot)
            except ValueError:
                pass

        snapshots.sort()

        # choose version
        if use_last_version:
            version = snapshots[-1]

        else:

            prompt = "Choose version for mediapackage {} from {}: ".format(mp_id, ", ".join(map(str, snapshots)))
            invalid = "This version is not available for mediapackage {}.".format(mp_id)
            version = get_number(prompt, invalid, snapshots)

        version_dir = os.path.join(mp_dir, str(version))

        mps_to_recover.append(MediaPackage(id=mp_id, version=version, path=version_dir))

    return sorted(mps_to_recover, key=attrgetter('id'))
