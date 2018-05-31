import re
import requests
import sys
from datetime import datetime
from dateutil.parser import parse

URL = 'https://api.github.com/repos/opencast/opencast/pulls' \
      '?state=closed&base='


def main(branch, start_date):
    begin = parse(start_date).replace(tzinfo=None)
    end = datetime.now()
    next_url = URL + branch
    pullrequests = []

    # get all closed pull request for a specific branch
    while next_url:
        r = requests.get(next_url)
        link_header = r.headers.get('Link')
        next_url = None
        if link_header:
            match = re.search('<([^>]*)>; rel="next"', link_header)
            if match:
                next_url = match.group(1)
        pullrequests += r.json()

    # filter by merge date
    for pr in pullrequests:
        merged = pr.get('merged_at')
        if not merged:
            continue  # pull request was canceled
        merged = parse(merged).replace(tzinfo=None)
        if begin < merged < end:
            link = pr.get('html_url')
            title = pr.get('title')
            print('- [%s\n  ](%s)' % (title, link))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: %s branch start-date' % sys.argv[0])
    else:
        main(sys.argv[1], sys.argv[2])
