import os
import sys

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

import config
# from data_handling.elements import get_id
# from data_handling.errors import MediaPackageError
# from data_handling.parse_manifest import parse_manifest_from_endpoint
# from import_mp.import_mp import import_mp
# from input_output.input import get_yes_no_answer
# from rest_requests.api_requests import get_events_of_series
# from rest_requests.assetmanager_requests import get_media_package
from rest_requests.request import get_request, post_request
from rest_requests.request_error import RequestError
from parse_args import parse_args
from args.digest_login import DigestLogin


def main():
    """
    Populate the specified Opencast system with random sample events
    """

    # use api/events/{id}

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
    response = get_request(url, digest_login, "events")
    print(response.json())

    for i in range(number_of_events):
        try:
            # create event
            url = f'{target_url}/api/info/me'

            data = {

            }
            response = post_request(url, digest_login, "events", data=data)
            print(response.json())

        except Exception as e:
            print("ERROR")
            print(str(e))

    print("Done.")


def __abort_script(message):
    print(message)
    sys.exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
