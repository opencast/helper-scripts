    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from httpx import Timeout

from opencast.assetmanager import get_mediapackage
from opencast.client import OpencastClient
from opencast.externalapi import get_events


class AssetmanagerTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(AssetmanagerTestCase, self).__init__(*args, **kwargs)
        self.hostname = 'https://develop.opencast.org'
        self.username = 'admin'
        self.password = 'opencast'

    def test_get_mediapackage(self):
        with OpencastClient(self.hostname, auth=(self.username, self.password), timeout=Timeout(5.0)) as opencast_client:
            for event in get_events(opencast_client):
                mp = get_mediapackage(opencast_client, event['identifier'])
                self.assertEqual(mp.get_identifier(), event['identifier'])
                break


if __name__ == '__main__':
    unittest.main()
