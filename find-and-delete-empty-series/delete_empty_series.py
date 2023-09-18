import os
import sys

from input_output.read_file import read_list_from_file, write_list_to_file
from rest_requests.request_error import RequestError

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

import config
from args.digest_login import DigestLogin
from rest_requests.series_requests import delete_series, series_has_events


def delete_empty_series(admin_url, digest_login, empty_series):
    deleted_series = []
    for series_id in empty_series:
        try:
            if series_has_events(admin_url, digest_login, series_id):
                print("Series {} has events, not deleting!".format(series_id))
                continue
            delete_series(admin_url, digest_login, series_id)
            deleted_series.append(series_id)
        except RequestError as e:
            print("Series {} could not be deleted: {}", series_id, e)
    return deleted_series


def main():
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)
    empty_series = read_list_from_file("empty_series.txt")
    print("{} empty series found.".format(len(empty_series)))

    deleted_series = delete_empty_series(config.admin_url, digest_login, empty_series)
    write_list_to_file("deleted_series.txt", deleted_series)
    print("Deletion finished. {} series were successfully deleted.".format(len(deleted_series)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
