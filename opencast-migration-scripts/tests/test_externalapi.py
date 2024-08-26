#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from httpx import Timeout

from opencast.client import OpencastClient
from opencast.externalapi import get_info_me, get_series, get_events


class ExternalapiTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ExternalapiTestCase, self).__init__(*args, **kwargs)
        self.hostname = 'https://develop.opencast.org'
        self.username = 'admin'
        self.password = 'opencast'

    def test_info_me(self):
        with OpencastClient(self.hostname, auth=(self.username, self.password), timeout=Timeout(5.0)) as opencast_client:
            me = get_info_me(opencast_client)
            self.assertIn('username', me.keys())
            self.assertEqual(me.get('username'), 'admin')

    def test_get_series(self):
        with OpencastClient(self.hostname, auth=(self.username, self.password), timeout=Timeout(5.0)) as opencast_client:
            series = get_series(opencast_client)
            for s in series:
                self.assertIn('identifier', s.keys())
                self.assertIn('title', s.keys())
                self.assertIn('creator', s.keys())
                self.assertIn('created', s.keys())
                # print('\t'.join([s['created'], s['identifier'], s['title']]))

    def test_get_events(self):
        with OpencastClient(self.hostname, auth=(self.username, self.password), timeout=Timeout(5.0)) as opencast_client:
            events = get_events(opencast_client)
            for event in events:
                self.assertIn('identifier', event.keys())
                self.assertIn('title', event.keys())
                self.assertIn('creator', event.keys())
                self.assertIn('created', event.keys())
                # print('\t'.join([event['created'], event['identifier'], event['title']]))


if __name__ == '__main__':
    unittest.main()
