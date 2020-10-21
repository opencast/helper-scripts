import os

from input_output.read_file import read_file


def get_dummy_series_dc(series_id):
    """
    Get an empty series dublin core catalog with the given id.

    :param series_id: The series ID
    :type series_id: str
    :return: A dummy series dublin core catalog
    :rtype: str
    """

    dummy_series_dc = os.path.abspath("dummy_series_dc.xml")
    content = read_file(dummy_series_dc)
    content_first, content_second = content.split("*")
    content = content_first + series_id + content_second
    return content
