import os
import sys

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

import config
from rest_requests.request import get_request, post_request, big_post_request
from rest_requests.request_error import RequestError
from parse_args import parse_args
from args.digest_login import DigestLogin
import string
import random


def main():
    """
    Populate the specified Opencast system with random sample events
    """

    target_url, number_of_events, file_path = parse_args()
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)

    if not target_url:
        target_url = config.target_url
    if not number_of_events:
        number_of_events = config.number_of_events
    if not file_path:
        file_path = config.test_video_path

    print(number_of_events)
    print(target_url)

    print("Starting population process.")

    # test API connection
    url = f'{target_url}/api/info/me'
    try:
        get_request(url, digest_login, "events")
    except:
        __abort_script("Something went wrong. No Connection to API. Stopping script. ")

    # Serien erstellen
    series = []

    for i in range(config.number_of_series):

        url = f'{target_url}/series/'
        id = __generate_random_name()
        series.append(id)
        data = {
            'identifier': id,
            'publisher': __generate_random_name(),
            'title': __generate_random_name(),
            'acl': '{"acl": {"ace": ['
                   '{"allow": true,"role": "ROLE_ANONYMOUS","action": "write"}, '
                   '{"allow": true,"role": "ROLE_ADMIN","action": "read"}'
                   ']}}'
        }

        try:
            response = post_request(url, digest_login, "series", data=data)
            print(response)

        except Exception as e:
            print("ERROR")
            print(str(e))
            __abort_script("Something went wrong. Could not create series. Stopping script")

    # Events erstellen
    for i in range(number_of_events):

        url = f'{target_url}/ingest/addMediaPackage'    # schedule-and-upload
        files = [file_path]

        data = {
            'creator': __generate_random_name(),
            'title': __generate_random_name(),
            'flavor': 'presentation/source',
            'description': 'This is a test description. This Event is only for testing purposes. ',
            'spatial': __generate_random_name(),
            'isPartOf': random.choice(series),
            'acl': '{"acl": {"ace": ['
                   '{"allow": true,"role": "ROLE_ADMIN","action": "read"}, '
                   '{"allow": true,"role": "ROLE_ADMIN","action": "write"}, '
                   '{"allow": true,"role": "ROLE_ANONYMOUS","action": "read"}'
                   ']}}'
        }

        try:
            response = big_post_request(url, digest_login, "events", data=data, files=files)
            print(response)

        except Exception as e:
            print("ERROR")
            print(str(e))
            __abort_script("Something went wrong. Could not create event. Stopping script")

        # ToDo copy the Events

    print("Done.")


def __create_alphabet():
    alphabet = list(string.ascii_letters)
    for i in range(10):
        alphabet.append(str(i))
    for c in ['Ä','Ö','Ü','ä','ö','ü']:
        alphabet.append(c)
    return alphabet

alphabet = __create_alphabet()


def __generate_random_name():
    name = ''
    for i in range(random.randint(1, 30)):
        name += random.choice(alphabet)
    return name


def __abort_script(message):
    print(message)
    sys.exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
