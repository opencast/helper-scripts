from input_output.input import get_configurable_answer
from utility.enum import enum

FixAnswer = enum(
    NEXT="n",
    ALL="a",
    REST="r",
    SKIP="s",
    QUIT="q"
)


def fix_question(level=0):
    """
    Ask user the question whether they want to fix one/more element(s) to give them the chance to change their mind,
    skip some errors or check previous fixes for correctness before continuing.

    :return: The answer.
    :rtype: FixAnswer
    """

    long_descriptions = ["fixing the next event with this error of the current tenant",
                         "fixing all remaining events with this errors of the current tenant",
                         "fixing all events with all errors for all tenants without asking again",
                         "skipping the rest of the events with this error of the current tenant",
                         "quitting the script completely"]
    short_descriptions = ["next", "remaining", "all", "skip", "quit"]
    options = ['n', 'r', 'a', 's', 'q']
    question = "Fix?"

    answer = get_configurable_answer(options, short_descriptions, long_descriptions, question, level)
    return answer
