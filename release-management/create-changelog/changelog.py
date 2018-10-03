import re
import requests
import sys
from datetime import datetime
from dateutil.parser import parse

URL = 'https://api.github.com/repos/opencast/opencast/pulls' \
      '?state=closed&base='
JIRA_TICKET_URL = 'https://opencast.jira.com/browse/'


def main(branch, start_date, end_date):
    begin = parse(start_date).replace(tzinfo=None)
    end = parse(end_date).replace(tzinfo=None) if end_date else datetime.now()
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
        if begin <= merged <= end:
            link = pr.get('html_url')
            title = pr.get('title')
            nr = pr.get('number')
            pretty_print(title, nr, link)


def pretty_print(title, pr_number, pr_link):
    title_re = '^[tTfF]?/?(?:mh|MH)[- ]+(?P<ticketNr>\d{5})\W*(?P<prTitle>.*)$'
    m = re.search(title_re, title)
    if m:
        ticket = m.group('ticketNr')
        ticket_url = '%sMH-%s' % (JIRA_TICKET_URL, ticket)
        pr_title = m.group('prTitle')
        print('- [[MH-%s](%s)][[#%s](%s)] -\n  %s'
              % (ticket, ticket_url, pr_number, pr_link, pr_title))
    else:
        print('- [%s\n  ](%s)' % (title, pr_link))


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 3 or argc > 4:
        print('Usage: %s branch start-date [end-date]' % sys.argv[0])
    else:
        branch = sys.argv[1]
        start_date = sys.argv[2]
        end_date = None
        if argc == 4:
            end_date = sys.argv[3]

        main(branch, start_date, end_date)
