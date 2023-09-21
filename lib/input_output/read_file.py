import io


def read_file(file_path):
    """
    Return the content of a file as a string without newlines.

    :param file_path: The path to the file
    :type file_path: str
    :return: File content
    :rtype: str
    """

    file_string = ''

    with io.open(file_path, 'r', newline='', encoding='utf8') as file:
        for line in file:
            file_string = file_string + line.rstrip('\n')

    return file_string


def write_list_to_file(file_path, list):
    """
    Write each item of a list into a new line of the file.

    :param file_path: The path to the file
    :type file_path: str
    :param list: A list of strings to write
    :type list: list
    """

    with io.open(file_path, 'w', encoding='utf8') as file:
        for item in list:
            file.write("{}\n".format(item))


def read_list_from_file(file_path):
    """
    Read list of strings from a file where each item is on a new line.

    :param file_path: The path to the file
    :type file_path: str
    :return: File content
    :rtype: list
    """

    with io.open(file_path, 'r', encoding='utf8') as file:
        return file.read().splitlines()
