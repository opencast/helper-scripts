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

    # Auth?
    headers = {'Authorization': f'Bearer {pat}'} if pat else {}

    # get all closed pull request for a specific branch
    while next_url:
        result = requests.get(next_url, headers=headers)
        link_header = result.headers.get('Link')
        next_url = None
        if link_header:
            match = re.search('<([^>]*)>; rel="next"', link_header)
            if match:
                next_url = match.group(1)
        pullrequests += result.json()

    # filter by merge date
    bot_pullrequests = []
    for pr in pullrequests:
        merged = pr.get('merged_at')
        if not merged:
            continue  # pull request was canceled
        merged = parse(merged).replace(tzinfo=None)
        if begin <= merged <= end:
            # Print (dependa-)bot pull requests seperately
            user_type = pr.get('user').get('type')
            if user_type == 'Bot':
                bot_pullrequests.append(pr)
                continue

            link = pr.get('html_url')
            title = pr.get('title').strip()
            nr = pr.get('number')
            pretty_print(title, nr, link)

    if len(bot_pullrequests) > 0:
        print('<details><summary>Bot Pull Requests</summary>\n')
        print('<ul>')
        for bot_pr in bot_pullrequests:
            link = bot_pr.get('html_url')
            title = bot_pr.get('title').strip()
            nr = bot_pr.get('number')
            bot_pretty_print(title, nr, link)
        print('</ul>')
        print('</details>')


def pretty_print(title, pr_number, pr_link):
    title = pretty_print_title(title)
    print('- [[#%s](%s)] -\n  %s' % (pr_number, pr_link, title))

def bot_pretty_print(title, pr_number, pr_link):
    title = pretty_print_title(title)
    print('<li>[<a href="%s">%s</a>] - \n  %s</li>' % (pr_link, pr_number, title))

def pretty_print_title(title):
    return re.sub(r'^\S*[mM][hH]-\d{3,5}[,: ]*', '', title)

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
        binary = sys.argv[0]
        print(f'Usage: {binary} branch start-date [end-date] [github pat]')
