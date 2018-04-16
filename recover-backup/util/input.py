"""
This module provides functionality to get additional input from the user.
"""

def get_yes_no_answer(question):
    """
    Ask user a yes/no-question.

    :param question: The question.
    :type question: str
    :return: The answer.
    :rtype: bool
    """

    while True:

        answer = input(question + " [y/n]").lower()

        if answer == "y" or answer == "yes":
            return True
        elif answer == "n" or answer == "no":
            return False
        else:
            print("Invalid answer.")

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
            number = int(
                input(prompt)) # TODO

            if number in valid_numbers or not valid_numbers:
                return number
            else:
                print(invalid) # TODO

        except ValueError:
            print("Input has to be a number!")