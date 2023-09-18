import os
import sys
import time

from input_output.read_file import write_list_to_file
from rest_requests.request_error import RequestError

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

import config
from args.digest_login import DigestLogin
from rest_requests.basic_requests import get_series
from data_handling.elements import get_id
from rest_requests.series_requests import series_has_events


def find_empty_series(admin_url, digest_login):

    empty_series = []
    series_errors = []
    all_series = get_series(admin_url, digest_login)
    print("Obtained {} series.".format(len(all_series)))

    for i, series in enumerate(all_series):
        series_id = get_id(series)
        try:
            if not series_has_events(admin_url, digest_login, series_id):
                empty_series.append(series_id)
        except RequestError as e:
            print("Series {} could not be checked: {}".format(series_id, e))
            series_errors.append(series_id)
        if (i + 1) % 100 == 0:
            print("Checked {} series.".format(i + 1))
            time.sleep(1)
    print("{} empty series, {} series could not be checked".format(len(empty_series), len(series_errors)))
    return empty_series, series_errors


def main():
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)
    empty_series, series_errors = find_empty_series(config.admin_url, digest_login)
    print("Empty series: {}".format(len(empty_series)))

    if empty_series:
        write_list_to_file("empty_series.txt", empty_series)
    if series_errors:
        write_list_to_file("series_errors.txt", series_errors)
    print("Check finished.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
