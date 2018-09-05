def read_file(file_path):
    """
    Return the content of a file as a string without newlines.

    :param file_path: The path to the file
    :type file_path: str
    :return: File content
    :rtype: str
    """

    file_string = ''

    with open(file_path, 'r', newline='') as file:
        for line in file:
            file_string = file_string + line.rstrip('\n')

    return file_string
