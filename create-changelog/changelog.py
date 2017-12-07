#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


def main():
    try:
        with open('changelog.html', 'r') as f:
            html_doc = f.read()
    except IOError:
        print('Please save the following page as changelog.html')
        print('- Make sure you are logged in!')
        print('- Adjust the version if necessary')
        print('https://opencast.jira.com'
              '/sr/jira.issueviews:searchrequest-printable/temp'
              '/SearchRequest.html?jqlQuery=project+%3D+Opencast+AND'
              '+fixVersion+%3D+3.2+AND+status+%3D+Resolved+and'
              '+resolution+%3D+%22Fixed+and+reviewed%22&tempMax=1000')
        return
    soup = BeautifulSoup(html_doc, 'html.parser')
    for issue in soup.find_all(**{'class': 'issuerow'}):
        key = issue.get('data-issuekey')
        link = issue.find(**{'class': 'issuekey'}).a.get('href')
        summary = issue.find(**{'class': 'summary'}).get_text().strip()
        summary = summary.replace('\n', ' / ')
        print('- [[%s]](%s) - %s' % (key, link, summary))


if __name__ == '__main__':
    main()
