import os
from collections import defaultdict


def find_distribution_artefacts(distribution_dirs, tenants, progress_printer):
    """
    Find all distribution artefacts in the given directories belonging to the given tenants and return them by
    media package and tenant.

    :param distribution_dirs: Paths to the directories containing distribution artefacts.
    :type distribution_dirs: list
    :param tenants: The tenants for which distribution artefacts should be collected.
    :type tenants: list
    :param progress_printer: Object to print progress messages with.
    :type progress_printer: ProgressPrinter
    :return: The distribution artefacts by tenant and media package.
    :rtype: dict
    """

    progress_printer.begin_progress_message("Searching for distribution artefacts... ")
    distribution_artefacts = defaultdict(lambda: defaultdict(list))
    count = 0

    for distribution_dir_count, distribution_dir in enumerate(distribution_dirs):

        dir_name, tenant_dirs, files = next(os.walk(distribution_dir))

        for tenant_count, tenant in enumerate(tenant_dirs):

            tenant_dir = os.path.join(distribution_dir, tenant)

            if tenant in tenants:
                dir_name, channel_dirs, files = next(os.walk(tenant_dir))

                for channel_count, channel in enumerate(channel_dirs):

                    channel_dir = os.path.join(tenant_dir, channel)
                    dir_name, media_packages, files = next(os.walk(channel_dir))

                    progress_printer.print_progress_message("Directory {}/{}, tenant {}/{}, channel {}/{}".
                                                            format(distribution_dir_count + 1, len(distribution_dirs),
                                                                   tenant_count + 1, len(tenant_dirs),
                                                                   channel_count + 1, len(channel_dirs)))

                    for media_package in media_packages:
                        media_package_dir = os.path.join(channel_dir, media_package)

                        distribution_artefacts[tenant][media_package].append(media_package_dir)
                        count += 1

    progress_printer.end_progress_message("{} distribution artefact(s) found.\n".format(count))

    return distribution_artefacts
