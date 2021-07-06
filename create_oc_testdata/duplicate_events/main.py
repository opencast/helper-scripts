import os
import sys

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

import config
from rest_requests.request import get_request, post_request, big_post_request
from parse_args import parse_args
from args.digest_login import DigestLogin
import yaml


def main():
    """
    Duplicate the events on the specified Opencast system defined in the yaml file
    """

    target_url, number_of_events, file_path = parse_args()
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)

    target_url = target_url if target_url else config.target_url
    number_of_duplicates = number_of_events if number_of_events else config.number_of_duplicates
    file_path = file_path if file_path else config.yaml_file_path

    print("Starting duplication process.")

    # test API connection
    url = f'{target_url}/api/info/me'
    try:
        get_request(url, digest_login, "events")
    except:
        __abort_script("Something went wrong. No Connection to API. Stopping script. ")

    # read IDs from file
    event_ids = read_event_ids(file_path)

    # duplicate events
    url = f'{target_url}/api/workflows/'

    for id in event_ids:
        print(id)
        data = {
            'event_identifier': id,
            'workflow_definition_identifier': 'duplicate-event',
            'configuration': '{"numberOfEvents":"' + str(number_of_duplicates) + '"}'
        }
        try:
            response = post_request(url, digest_login, "events", data=data)
            print(response)
        except Exception as e:
            print(str(e))
            __abort_script("Something went wrong. Could not duplicate event. Stopping script")

    print("Done.")


def read_event_ids(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    return data['event-IDs']


def __abort_script(message):
    print(message)
    sys.exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
