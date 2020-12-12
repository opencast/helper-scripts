from rest_requests.get_response_content import get_string_content
from rest_requests.request import get_request


def get_file_as_string(digest_login, url):
    """
    Get the file content as a string

    :param url: The url to the file
    :type url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :return: The file content
    :rtype: str
    :raise RequestError:
    """

    response = get_request(url, digest_login, "file")
    return get_string_content(response)


def get_video_file(digest_login, url, target_file):
    """
    Request a video and write it into a file.

    :param url: The url to the file
    :type url: str
    :param digest_login: The login credentials for digest authentication
    :type digest_login: DigestLogin
    :param target_file: The file to write into
    :type target_file: Path
    :return: The file content
    :rtype: str
    :raise RequestError:
    """

    response = get_request(url, digest_login, "video", stream=True)

    with open(target_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
