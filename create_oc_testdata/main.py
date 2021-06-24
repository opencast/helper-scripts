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


alphabet = list(string.ascii_letters)
for i in range(10):
    alphabet.append(str(i))
for c in ['Ä','Ö','Ü','ä','ö','ü']:
    alphabet.append(c)


def main():
    """
    Populate the specified Opencast system with random sample events
    """

    # use api/events/{id} ?

    target_url, number_of_events = parse_args()
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)

    if not target_url:
        target_url = config.target_url
    if not number_of_events:
        number_of_events = config.number_of_events

    print(number_of_events)
    print(target_url)

    print("Starting population process.")

    # test request
    url = f'{target_url}/api/info/me'
    try:
        response = get_request(url, digest_login, "events")
    except:
        __abort_script("Something went wrong. No Connection to API. Stopping script. ")

    for i in range(number_of_events):
        try:
            # create event
            url = f'{target_url}/ingest/addMediaPackage/fast'
            files = [config.test_video_path]

            data = {
                'creator': __generate_random_name(),
                'title': __generate_random_name(),
                'flavor': 'presentation/source',
                'acl': '{"acl": {"ace": [{"allow": true,"role": "ROLE_Z","action": "dance"}]}}'
            }

            response = big_post_request(url, digest_login, "events", data=data, files=files)
            print(response)

        except Exception as e:
            print("ERROR")
            print(str(e))
            __abort_script("Something went wrong. Could not create event. Stopping script")

        print("Done.")


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
