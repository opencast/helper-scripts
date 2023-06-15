import re
import requests
import sys
from datetime import datetime
from dateutil.parser import parse

URL = 'https://api.github.com/repos/opencast/opencast/pulls' \
      '?state=closed&base='
JIRA_TICKET_URL = 'https://opencast.jira.com/browse/'


def main(branch, start_date, end_date, pat):
    begin = parse(start_date).replace(tzinfo=None)
    end = parse(end_date).replace(tzinfo=None) if end_date else datetime.now()
    next_url = URL + branch
    pullrequests = []

    # get all closed pull request for a specific branch
    while next_url:
        r = None
        if None != pat:
            r = requests.get(next_url)
        else:
            r = requests.get(next_url, headers = {
                  "Authorization": "Bearer " + pat,
            })
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
        if begin <= merged <= end:
            link = pr.get('html_url')
            title = pr.get('title').strip()
            nr = pr.get('number')
            pretty_print(title, nr, link)


def pretty_print(title, pr_number, pr_link):
    title = re.sub(r'^\S*[mM][hH]-\d{3,5}[,: ]*', '', title)
    print('- [[#%s](%s)] -\n  %s' % (pr_number, pr_link, title))


if __name__ == '__main__':
    argc = len(sys.argv)
    if 3 <= argc <= 5:
        branch = sys.argv[1]
        start_date = sys.argv[2]
        end_date = None
        pat = None
        if argc >= 4:
            end_date = sys.argv[3]
        if argc == 5:
            pat = sys.argv[4]

        main(branch, start_date, end_date, pat)
    else:
        print('Usage: %s branch start-date [end-date] [github pat]' % sys.argv[0])
