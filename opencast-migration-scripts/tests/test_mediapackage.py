#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from opencast.mediapackage import Mediapackage


class MediapackageTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MediapackageTestCase, self).__init__(*args, **kwargs)
        import os
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testmp.xml', 'r', encoding='utf-8') as mp_xml_file:
            self.mediapackage_xml = mp_xml_file.read()
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testmp2.xml', 'r', encoding='utf-8') as mp_xml_file:
            self.mediapackage2_xml = mp_xml_file.read()

    def test_get_identifier(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        self.assertEqual(mediapackage.get_identifier(), 'ID-nasa-earth-4k')

    def test_get_title(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        self.assertEqual(mediapackage.get_title(), 'View of Planet Earth (4K)')

    def test_apply_tags_absolute(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        mediapackage.apply_tags(['foo', 'bar'])
        mediapackage.remove_publication()   # remove all publications (and their tags)
        # print(mediapackage)
        self.assertIn('<tag>foo</tag>', str(mediapackage))
        self.assertIn('<tag>bar</tag>', str(mediapackage))
        self.assertNotIn('<tag>archive</tag>', str(mediapackage))

    def test_apply_tags_append(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        mediapackage.apply_tags(['+foo', '+archive'])
        mediapackage.remove_publication()   # remove all publications (and their tags)
        # print(mediapackage)
        self.assertIn('<tag>foo</tag>', str(mediapackage))
        self.assertIn('<tag>archive</tag>', str(mediapackage))

    def test_apply_tags_append_with_element_filter(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        test_element_filter = lambda element: element.tag.endswith('attachment') and \
                                              element.get('type') == 'security/xacml+series'
        mediapackage.apply_tags(['+foo'], element_filter=test_element_filter)
        mediapackage.remove_publication()   # remove all publications (and their tags)
        self.assertEqual(len(mediapackage.get_attachments()), 2)
        for attachment in mediapackage.get_attachments():
            if attachment.get_flavor() == 'security/xacml+series':
                self.assertIn('foo', attachment.get_tags())
            else:
                self.assertNotIn('foo', attachment.get_tags())

    def test_apply_tags_remove(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        mediapackage.apply_tags(['-archive'])
        mediapackage.remove_publication()   # remove all publications (and their tags)
        # print(mediapackage)
        self.assertNotIn('<tag>archive</tag>', str(mediapackage))

    def test_merge(self):
        mediapackage1 = Mediapackage(self.mediapackage_xml)
        mediapackage2 = Mediapackage(self.mediapackage2_xml)
        mediapackage2.remove_publication()
        mediapackage2.apply_tags(tags=['search'])
        self.assertIn('<tag>search</tag>', str(mediapackage2))
        self.assertNotIn('<tag>search</tag>', str(mediapackage1))
        mediapackage1.merge(mediapackage2)
        # print(mediapackage1)
        self.assertIn('<tag>search</tag>', str(mediapackage1))

    def test_get_attachments(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        attachments = mediapackage.get_attachments()
        self.assertEqual(len(attachments), 2)
        self.assertIn(attachments[0].get_flavor(), ['security/xacml+episode', 'security/xacml+series'])
        self.assertIn(attachments[1].get_flavor(), ['security/xacml+episode', 'security/xacml+series'])

    def test_get_attachments_filtered(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        element_filter_episode_xacml = lambda element: element.get('type') == 'security/xacml+series'
        attachments = mediapackage.get_attachments(element_filter=element_filter_episode_xacml)
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].get_flavor(), 'security/xacml+series')

    def test_get_attachments_filtered_to_empty(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        element_filter_empty_result = lambda element: element.get('type') == 'foo/bar'
        attachments = mediapackage.get_attachments(element_filter=element_filter_empty_result)
        self.assertEqual(len(attachments), 0)

    def test_get_catalogs(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        catalogs = mediapackage.get_catalogs()
        self.assertEqual(len(catalogs), 1)
        self.assertEqual(catalogs[0].get_flavor(), 'dublincore/episode')

    def test_get_tracks(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        tracks = mediapackage.get_tracks()
        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0].get_flavor(), 'presenter/source')

    def test_get_track_tags(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        track = mediapackage.get_tracks()[0]
        tags = track.get_tags()
        self.assertEqual(len(tags), 1)
        self.assertIn('archive', tags)

    def test_get_catalog_url(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        catalogs = mediapackage.get_catalogs()
        self.assertEqual(len(catalogs), 1)
        catalog = catalogs[0]
        self.assertEqual(catalog.get_url(),
                         'https://develop.opencast.org/assets/assets/'
                         'ID-nasa-earth-4k/17e1fbe3-774b-4ebb-914b-7f4de94f0a20/1/dublincore.xml')

    def test_add_elements_from_publication(self):
        mediapackage = Mediapackage(self.mediapackage_xml)
        tracks = mediapackage.get_tracks()
        elements_added = mediapackage.add_elements_from_publication('internal',
                                                                    tags=['+test-tag', '+engage-download', '-default'])
        tracks_after_add = mediapackage.get_tracks()
        assert len(elements_added) > 0
        assert len(tracks) + len(elements_added) == len(tracks_after_add)
        element_tags = elements_added[0].get_tags()
        assert 'test-tag' in element_tags
        assert 'engage-download' in element_tags
        assert 'default' not in element_tags


if __name__ == '__main__':
    unittest.main()
