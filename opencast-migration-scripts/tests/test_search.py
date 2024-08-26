#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from httpx import Timeout

from opencast.client import OpencastClient
from opencast.externalapi import get_events
from opencast.search import get_mediapackage


class SearchTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(SearchTestCase, self).__init__(*args, **kwargs)
        self.hostname = 'https://develop.opencast.org'
        self.username = 'admin'
        self.password = 'opencast'

    def test_get_mediapackage(self):
        with OpencastClient(self.hostname, auth=(self.username, self.password), timeout=Timeout(5.0)) as opencast_client:
            events = get_events(opencast_client)
            for event in events:
                # get mediapackage from search service (if published)
                mediapackage = get_mediapackage(opencast_client, event['identifier'])
                if mediapackage:
                    # print(mediapackage)
                    self.assertEqual(event['identifier'], mediapackage.get_identifier())
                    return


if __name__ == '__main__':
    unittest.main()
