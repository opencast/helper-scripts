import shutil

from input.delete_question import DeleteAnswer, delete_question
from input.present_dead_distribution_artefacts import PresentAnswer
from util.count import count_distribution_artefacts


def delete_dead_distribution_artefacts(dead_distribution_artefacts, log_writer, progress_printer, present_answer):
    """
    Delete the dead distribution artefacts.

    :param dead_distribution_artefacts: The distribution artefacts to be deleted because their media packages no longer
    exist.
    :type dead_distribution_artefacts: dict
    :param log_writer: Object to write into the log
    :type log_writer: LogWriter
    :param progress_printer: Object to print progress bars.
    :type progress_printer: ProgressPrinter
    :param present_answer: The answer the user gave when all dead distribution artefacts were presented
    :type present_answer: str
    """
    count = 0

    dist_count = count_distribution_artefacts(dead_distribution_artefacts)

    state = DeleteAnswer.NEXT if present_answer == PresentAnswer.ASK else DeleteAnswer.ALL

    if present_answer == PresentAnswer.DELETE:
        progress_printer.print_message("Deleting all distribution artefacts...")

    for tenant in dead_distribution_artefacts.keys():

        for media_package in dead_distribution_artefacts[tenant].keys():

            if state == DeleteAnswer.NEXT:
                state = delete_question(media_package)

                if state == DeleteAnswer.QUIT:
                    return
                elif state == DeleteAnswer.ALL:
                    progress_printer.print_message("Deleting remaining distribution artefacts...")
                    dist_count -= count
                    count = 0

            if (present_answer == PresentAnswer.DELETE or state == DeleteAnswer.ALL) and count == 0:
                progress_printer.print_progress(count, dist_count)

            for distribution_artefact in dead_distribution_artefacts[tenant][media_package]:

                shutil.rmtree(distribution_artefact, ignore_errors=True)
                log_writer.write_to_log(tenant, media_package, distribution_artefact)
                count += 1

                if present_answer == PresentAnswer.DELETE or state == DeleteAnswer.ALL:
                    progress_printer.print_progress(count, dist_count)

            if present_answer == PresentAnswer.ASK and not state == DeleteAnswer.ALL:
                progress_printer.print_message("Distribution artefacts of media package {} deleted.\n"
                                               .format(media_package))
