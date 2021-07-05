import os
import sys

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

import config
from rest_requests.request import get_request, post_request, big_post_request
from parse_args import parse_args
from args.digest_login import DigestLogin
import yaml
import string
import random


def main():
    """
    Populate the specified Opencast system with random sample events
    """

    target_url, number_of_events, file_path = parse_args()
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)

    target_url = target_url if target_url else config.target_url
    number_of_events = number_of_events if number_of_events else config.number_of_events
    file_path = file_path if file_path else config.test_video_path

    print("Starting population process.")

    # test API connection
    url = f'{target_url}/api/info/me'
    try:
        get_request(url, digest_login, "events")
    except:
        __abort_script("Something went wrong. No Connection to API. Stopping script. ")

    # Serien erstellen
    series_ids = []
    for i in range(config.number_of_series):
        url = f'{target_url}/series/'
        series_id = "Series-ID-" + __generate_random_name()
        series_ids.append(series_id)
        data = {
            'identifier': series_id,
            'publisher': __generate_random_name(),
            'title': __generate_random_name(),
            'acl': '{"acl": {"ace": ['
                   '{"allow": true,"role": "ROLE_ANONYMOUS","action": "write"}, '
                   '{"allow": true,"role": "ROLE_ADMIN","action": "read"}'
                   ']}}'
        }
        try:
            print(post_request(url, digest_login, "series", data=data))
            # print(response)
        except Exception as e:
            print(str(e))
            __abort_script("Something went wrong. Could not create series. Stopping script")

    # Events erstellen
    event_ids = []
    url = f'{target_url}/ingest/addMediaPackage'
    files = [file_path]

    for i in range(number_of_events):

        event_id = "ID-" + __generate_random_name(length=5)
        event_ids.append(event_id)

        data = {
            'creator': __generate_random_name(),
            'title': __generate_random_name(),
            'flavor': 'presentation/source',
            'description': 'This is a test description. This Event is only for testing purposes. ',
            'identifier': event_id,
            'spatial': __generate_random_name(),
            'isPartOf': random.choice(series_ids),
            'acl':  '{"acl": {"ace": ['
                        '{"allow": true,"role": "ROLE_ADMIN","action": "read"}, '
                        '{"allow": true,"role": "ROLE_ADMIN","action": "write"}'
                    ']}}'
        }

        try:
            response = big_post_request(url, digest_login, "events", data=data, files=files)
            print(response)
        except Exception as e:
            print(str(e))
            __abort_script("Something went wrong. Could not create event. Stopping script")

    # write event IDs to yaml file
    yaml_content = {'event-IDs': event_ids}
    with open(config.yaml_file_path, 'w') as file:
        yaml.dump(yaml_content, file)

    print("Done.")


def __create_alphabet():
    alphabet = list(string.ascii_letters)
    # for i in range(10):
    #     alphabet.append(str(i))
    # for c in ['Ä','Ö','Ü','ä','ö','ü']:
    #     alphabet.append(c)
    return alphabet

alphabet = __create_alphabet()


def __generate_random_name(length=False):
    name = ''
    length = length if length else random.randint(1, 30)
    for i in range(length):
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
