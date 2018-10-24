"""
This module provides functionality to get additional input_output from the user.
"""
from input_output.progress_printer import ProgressPrinter


def get_yes_no_answer(question):
    """
    Ask user a yes/no-question.

    :param question: The question.
    :type question: str
    :return: The answer.
    :rtype: bool
    """

    while True:

        answer = input(question + " [y/n] ").lower()

        if answer == "y" or answer == "yes":
            return True
        elif answer == "n" or answer == "no":
            return False
        else:
            print("Invalid answer.")


def __create_help_description(indent, options, long_descriptions):
    """
    Create a description that is shown for the help option.

    :param indent: How much to indent the description.
    :type indent: str
    :param options: The available options.
    :type options: list
    :param long_descriptions: Long descriptions for all options.
    :type long_descriptions: list
    :return: The help description.
    :rtype: str
    """

    help_description = "\n{}Valid answers are".format(indent)

    for option, long_description in zip(options, long_descriptions):
        help_description += "\n{}'{}' for {}".format(indent, option, long_description)

    help_description += ": "
    return help_description


def __create_question(indent, question, options, short_descriptions):
    """
    Build the question by attaching the available options with short descriptions.

    :param indent: How much to indent the description.
    :type indent: str
    :param question: The question to ask the user.
    :type question: str
    :param options: The available options.
    :type options: list
    :param short_descriptions: Short descriptions for all options.
    :type short_descriptions: list
    :return: The question with short descriptions for the available options.
    :rtype: str
    """

    input_question = "{}{} Valid answers are ".format(indent, question)
    for count, (option, short_description) in enumerate(zip(options, short_descriptions)):
        input_question += "'{}' ({})".format(option, short_description)

        if count == len(options) - 1:
            input_question += ": "
        else:
            input_question += ", "

    return input_question


def get_configurable_answer(options, short_descriptions, long_descriptions, question, level=0):
    """
    Ask user a configurable question.

    :param options: The available options.
    :type options: list
    :param short_descriptions: Short descriptions for all options.
    :type short_descriptions: list
    :param long_descriptions: Long descriptions for all options.
    :type long_descriptions: list
    :param question: The question to ask the user.
    :type question: str
    :param level: The level to indent the message to
    :type level: int
    :return: The option chosen by the user.
    :rtype: str
    """

    help_option = 'h'
    if help_option in options:
        raise ValueError("'h' is a reserved option")

    options.append(help_option)
    short_descriptions.append('help')
    long_descriptions.append('printing a more detailed description of the options')

    indent = ProgressPrinter.get_indent(level)
    answer = ''

    help_description = __create_help_description(indent, options, long_descriptions)
    input_question = __create_question(indent, question, options, short_descriptions)

    while True:

        if answer == help_option:  # give a more detailed description of the options
            answer = input(help_description)

        else:  # ask the question
            answer = input(input_question).lower()

        # invalid answer?
        if answer not in options:
            print("{}Invalid answer.\n".format(indent))

        elif answer != help_option:

            print()
            return answer


def get_number(prompt, invalid, valid_numbers):
    """
    Ask the user for a number, can check for validity.

    :param prompt: The prompt.
    :type prompt: str
    :param invalid: What to print on an invalid answer.
    :type invalid: str
    :param valid_numbers: List of valid numbers
    :type valid_numbers: list or None
    :return: A valid number.
    :rtype: int
    """

    while True:

        try:
            number = int(input(prompt))

            if number in valid_numbers or not valid_numbers:
                return number
            else:
                print(invalid)

        except ValueError:
            print("Input has to be a number!")
