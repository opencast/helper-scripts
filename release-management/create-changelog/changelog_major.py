import sys
from dateutil.parser import parse

from lib.get_from_github import get_prs_from_github
from lib.print_pull_requests import print_pull_requests, filter_and_sort_prs


def create_changelog(version, last_branch_cut, this_branch_cut, last_release, this_release=None, gh_token=None):
    # parse args
    version = int(version)
    date_last_branch_cut = parse(last_branch_cut).replace(tzinfo=None)
    date_this_branch_cut = parse(this_branch_cut).replace(tzinfo=None)
    date_last_release = parse(last_release).replace(tzinfo=None)
    date_this_release_opt = parse(this_release).replace(tzinfo=None) if this_release else None

    # get PRs from GitHub
    pull_requests = get_prs_from_github(date_last_branch_cut, date_this_branch_cut, gh_token, 'develop')
    pull_requests += get_prs_from_github(date_this_branch_cut, date_this_release_opt, gh_token, version)

    legacy_pull_requests = get_prs_from_github(date_last_release, date_this_release_opt, gh_token, version - 1)
    for pr in legacy_pull_requests:
        pr['legacy'] = True
    pull_requests += legacy_pull_requests

    # print
    print_pull_requests(*filter_and_sort_prs(pull_requests))


if __name__ == '__main__':
    argc = len(sys.argv)
    if 5 <= argc <= 7:
        create_changelog(*sys.argv[1:])
    else:
        binary = sys.argv[0]
        print(f'Usage: {binary} version(int) last-branch-cut(date) this-branch-cut(date) last-release(date) '
              f'[this-release(date)] [github-token]')
