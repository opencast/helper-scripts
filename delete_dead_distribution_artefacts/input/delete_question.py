from input_output.input import get_configurable_answer
from utility.enum import enum

DeleteAnswer = enum(
    NEXT="n",
    ALL="a",
    QUIT="q"
)


def delete_question(media_package, level=0):
    """
    Ask user the question whether they want to delete the distribution artefacts for the next media package or for all
    remaining media packages.

    :param media_package: The media package to ask the question for
    :type: str
    :param level: The level to indent the question to
    :type level: int
    :return: The answer.
    :rtype: FixAnswer
    """

    long_descriptions = ["deleting the distribution artefacts of the next media package",
                         "deleting all(remaining) distribution artefacts",
                         "quitting the script"]
    short_descriptions = ["next", "all", "quit"]
    options = ['n', 'a', 'q']

    question = "Delete distribution artefacts of media package {}?".format(media_package)

    answer = get_configurable_answer(options, short_descriptions, long_descriptions, question, level)
    return answer
