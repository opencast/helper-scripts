""" This module finds the media packages in the backup that are to be recovered."""

from collections import namedtuple, OrderedDict
import os

from input_output.input import get_number

Snapshot = namedtuple('Snapshot', ["id", "version", "path"])


def find_media_packages(backup_path, tenant, use_last_version, rsync_history_path, media_package_ids=None):
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
    :param rsync_history_path: Path to rsync history
    :type rsync_history_path: str
    :return: List of media packages to be recovered containing their ids, the chosen version and path to the version
    directory
    :rtype: list
    """

    tenant_dir = __get_tenant_dir(backup_path, tenant)
    rsync_tenant_dirs = __get_rsync_tenant_dirs(rsync_history_path, tenant)

    if not tenant_dir and not rsync_tenant_dirs:
        print("No directories for tenant {} could be found.".format(tenant))
        return []

    if backup_path and not tenant_dir:
        print("Warning: No directory for tenant {} in archive backup found, checking rsync history only."
              .format(tenant))

    if rsync_history_path and not rsync_tenant_dirs:
        print("Warning: No directory for tenant {} in rsync history found.".format(tenant))

    if not media_package_ids:
        media_packages = __get_all_media_packages(tenant_dir, rsync_tenant_dirs)
    else:
        media_packages = __get_media_packages(media_package_ids, tenant_dir, rsync_tenant_dirs)

    mps_to_recover = []
    for mp_id, mp_dir in media_packages.items():

        snapshots = __find_snapshots(mp_dir)

        if len(snapshots) == 0:
            print("Media package {} at path {} does not contain any snapshots, skipped.".format(mp_id, mp_dir))
            continue

        version = __get_version(snapshots, mp_id, use_last_version)
        version_dir = os.path.join(mp_dir, str(version))

        mps_to_recover.append(Snapshot(id=mp_id, version=version, path=version_dir))

    return mps_to_recover


def __get_tenant_dir(backup_path, tenant):

    if backup_path:
        tenant_dir = os.path.join(backup_path, tenant)
        if os.path.isdir(tenant_dir):
            return tenant_dir
    return None


def __get_rsync_tenant_dirs(rsync_history_path, tenant):
    tenant_dirs = []

    if rsync_history_path:
        dir_name, date_dirs, files = next(os.walk(rsync_history_path))
        date_dirs = sorted(date_dirs, reverse=True)

        for date_dir in date_dirs:
            tenant_dir = os.path.join(rsync_history_path, date_dir, tenant)

            if os.path.isdir(tenant_dir):
                tenant_dirs.append(tenant_dir)

    return tenant_dirs


def __get_all_media_packages(tenant_dir, rsync_tenant_dirs):

    media_packages = None

    if tenant_dir:
        media_packages = __get_all_from_backup(tenant_dir)

    if rsync_tenant_dirs:
        rsync_media_packages = __get_all_from_rsync(rsync_tenant_dirs)

        if not media_packages:
            media_packages = rsync_media_packages
        else:
            for mp_id, mp_dir in rsync_media_packages.items():
                if mp_id not in media_packages:
                    media_packages[mp_id] = mp_dir

    return OrderedDict(sorted(media_packages.items()))


def __get_all_from_backup(tenant_dir):

    dir_name, sub_dirs, files = next(os.walk(tenant_dir))
    media_packages = OrderedDict((subdir, os.path.join(tenant_dir, subdir)) for subdir in sub_dirs)
    return media_packages


def __get_all_from_rsync(rsync_tenant_dirs):

    media_packages = OrderedDict()

    for tenant_dir in rsync_tenant_dirs:
        dir_name, sub_dirs, files = next(os.walk(tenant_dir))

        for subdir in sub_dirs:
            if subdir not in media_packages:
                media_packages[subdir] = os.path.join(tenant_dir, subdir)

    return media_packages


def __get_media_packages(media_package_ids, tenant_dir, rsync_tenant_dirs):

    media_packages = OrderedDict()
    for mp_id in media_package_ids:

        mp_dir = __find_mp_dir(mp_id, tenant_dir, rsync_tenant_dirs)

        if not mp_dir:
            print("Media package {} could not be found, skipped.".format(mp_id))
            continue

        media_packages[mp_id] = mp_dir

    return media_packages


def __find_mp_dir(mp_id, tenant_dir, rsync_tenant_dirs):

    mp_dir = None
    if tenant_dir:
        mp_dir = __check_backup_archive(mp_id, tenant_dir)

    if not mp_dir and rsync_tenant_dirs:
        mp_dir = __check_rsync_history(mp_id, rsync_tenant_dirs)

    return mp_dir


def __check_backup_archive(mp_id, tenant_dir):

    if tenant_dir:
        mp_dir = os.path.abspath(os.path.join(tenant_dir, mp_id))
        if os.path.isdir(mp_dir):
            return mp_dir
    return None


def __check_rsync_history(mp_id, rsync_tenant_dirs):

    for tenant_dir in rsync_tenant_dirs:
        mp_dir = os.path.abspath(os.path.join(tenant_dir, mp_id))
        if os.path.isdir(mp_dir):
            return mp_dir
    return None


def __find_snapshots(mp_dir):
    snapshots = []

    dir_name, sub_dirs, files = next(os.walk(mp_dir))

    if sub_dirs:
        for subdir in sub_dirs:
            try:
                snapshot = int(subdir)
                snapshots.append(snapshot)
            except ValueError:
                pass

    snapshots.sort()
    return snapshots


def __get_version(snapshots, mp_id, use_last_version):
    if use_last_version or len(snapshots) == 1:
        version = snapshots[-1]

    else:
        prompt = "Choose version for media package {} from {}: ".format(mp_id, ", ".join(map(str, snapshots)))
        invalid = "This version is not available for media package {}.".format(mp_id)
        version = get_number(prompt, invalid, snapshots)

    return version
