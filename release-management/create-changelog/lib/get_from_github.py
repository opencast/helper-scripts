import re
import requests
from dateutil.parser import parse


def get_branch(version):
    return 'r/' + str(version) + '.x'


def get_prs_from_github(start_date, end_date, pattern, branch):
    if isinstance(branch, int):
        branch = get_branch(branch)
    next_url = 'https://api.github.com/repos/opencast/opencast/pulls' \
               '?state=closed&sort=updated&direction=desc&per_page=100&base=' \
               + branch
    headers = {'Authorization': f'Bearer {pattern}'} if pattern else {}

    pull_requests = []
    while next_url:
        result = requests.get(next_url, headers=headers)
        parsed_results = result.json()
        # filter by merged date
        for pr in parsed_results:
            if pr.get('merged_at'):
                merged = parse(pr.get('merged_at')).replace(tzinfo=None)
                if start_date <= merged and (not end_date or merged <= end_date):
                    pr['merged_date'] = merged  # use the parsed merge date for sorting later
                    pull_requests.append(pr)

        # check if there are more
        next_url = None
        link_header = result.headers.get('Link')
        if link_header:
            match = re.search('<([^>]*)>; rel="next"', link_header)
            if match:
                next_url = match.group(1)

        # check when last pr in results was updated - if it's out of our desired date range, we can stop here
        # (all merges are updates, but not all updates are merges)
        updated = parse(parsed_results[-1].get('updated_at')).replace(tzinfo=None)
        if updated < start_date:
            next_url = None

    return pull_requests
