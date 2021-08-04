import os


def make_filename_unique(base_dir, file_name, file_extension):
    """
    Make sure filename is unique by checking if the file exists and appending a number if it does.

    :param base_dir: path to file
    :type base_dir: Path
    :param file_name: file name
    :type file_name: str
    :param file_extension: file extension
    :type file_extension: str
    :return: unique filename
    :rtype: str
    """
    counter = 1
    original_file_name = file_name
    path = os.path.join(base_dir, '{}.{}'.format(file_name, file_extension))
    while os.path.exists(path):
        file_name = original_file_name + "(" + str(counter) + ")"
        path = os.path.join(base_dir, '{}.{}'.format(file_name, file_extension))
        counter += 1
    return file_name


def make_dirname_unique(base_dir, dir_name):
    """
    Make sure directory name is unique by checking if the directory exists and appending a number if it does.

    :param base_dir: path to directory
    :type base_dir: Path
    :param dir_name: directory name
    :type dir_name: str
    :return: unique directory name
    :rtype: str
    """
    counter = 1
    original_dir_name = dir_name
    path = os.path.join(base_dir, dir_name)
    while os.path.exists(path):
        dir_name = original_dir_name + "(" + str(counter) + ")"
        path = os.path.join(base_dir, dir_name)
        counter += 1
    return dir_name
