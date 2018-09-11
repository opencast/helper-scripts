import shutil


def delete_dead_distribution_artefacts(dead_distribution_artefacts, log_writer, progress_printer):
    """
    Delete the dead distribution artefacts.

    :param dead_distribution_artefacts: The distribution artefacts to be deleted because their mediapackages no longer
    exist.
    :type dead_distribution_artefacts: dict
    :param log_writer: Object to write into the log
    :type log_writer: LogWriter
    :param progress_printer: Object to print progress bars.
    :type progress_printer: ProgressPrinter
    """

    total = sum([sum([len(dead_distribution_artefacts[tenant][media_package]) for media_package in
                      dead_distribution_artefacts[tenant].keys()]) for tenant in dead_distribution_artefacts.keys()])
    count = 0

    progress_printer.print_message("Deleting {} distribution artefacts... ".format(total), 0)

    for tenant in dead_distribution_artefacts.keys():

        for media_package in dead_distribution_artefacts[tenant].keys():

            for distribution_artefact in dead_distribution_artefacts[tenant][media_package]:

                shutil.rmtree(distribution_artefact, ignore_errors=True)
                log_writer.write_to_log(tenant, media_package, distribution_artefact)

                progress_printer.print_progress(count, total)
                count += 1
