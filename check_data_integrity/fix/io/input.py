from utility.enum import enum
from utility.progress_printer import ProgressPrinter

FixAnswer = enum(
    NEXT="n",
    ALL="a",
    REST="r",
    SKIP="s",
    QUIT="q",
    HELP="h"
)


def fix_question(no_fancy_output, level=0):
    """
    Ask user the question whether they want to fix one/more element(s) to give them the chance to change their mind,
    skip some errors or check previous fixes for correctness before continuing.

    :return: The answer.
    :rtype: FixAnswer
    """

    indent = ProgressPrinter.get_indent(level)
    answer = ''

    while True:

        if answer == FixAnswer.HELP:  # give a more detailed description of the options
            answer = input("\n{0}Valid answers are\n"
                           "{0}'n' for fixing the next event with this error of the current tenant\n"
                           "{0}'r' for fixing all remaining events with this errors of the current tenant\n"
                           "{0}'a' for fixing all events with all errors for all tenants without asking again\n"
                           "{0}'s' for skipping the rest of the events with this error of the current tenant\n"
                           "{0}'q' for quitting the script completely: ".format(indent))

        else:  # ask the question
            answer = input("{0}Fix? "
                           "Valid answers are 'n' (next), 'r' (remaining), 'a' (all), 's' (skip), 'q' (quit), "
                           "'h' (help): "
                           .format(indent)).lower()

        # invalid answer?
        if answer != FixAnswer.NEXT and answer != FixAnswer.REST and answer != FixAnswer.SKIP and \
                answer != FixAnswer.QUIT and answer != FixAnswer.HELP and answer != FixAnswer.ALL:
            print("{}Invalid answer.\n".format(indent))

        elif answer != FixAnswer.HELP:

            if not no_fancy_output:
                ProgressPrinter.clear_line()
                ProgressPrinter.back_to_previous_line()
                ProgressPrinter.back_to_previous_line()

            return answer
