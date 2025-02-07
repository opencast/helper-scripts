import sys
from dateutil.parser import parse

from lib.get_from_github import get_prs_from_github
from lib.print_pull_requests import print_pull_requests, filter_and_sort_prs


def create_changelog(version, include_legacy, start_date, end_date=None, gh_token=None):
    # parse args
    version = int(version)
    include_legacy = bool(include_legacy)
    date_last_release = parse(start_date).replace(tzinfo=None)
    date_this_release_opt = parse(end_date).replace(tzinfo=None) if end_date else None

    # get PRs from GitHub
    pull_requests = get_prs_from_github(date_last_release, date_this_release_opt, gh_token, version)

    # check prior version as well
    if include_legacy:
        legacy_pull_requests = get_prs_from_github(date_last_release, date_this_release_opt, gh_token, version - 1)
        for pr in legacy_pull_requests:
            pr['legacy'] = True
        pull_requests = pull_requests + legacy_pull_requests

    # print
    print_pull_requests(*filter_and_sort_prs(pull_requests))


if __name__ == '__main__':
    argc = len(sys.argv)
    if 4 <= argc <= 6:
        create_changelog(*sys.argv[1:])
    else:
        binary = sys.argv[0]
        print(f'Usage: {binary} version(int) include-legacy(bool) last-release(date) [this-release(date)]'
              f'[github-token]')
