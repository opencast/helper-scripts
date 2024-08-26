#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from copy import deepcopy
from uuid import uuid1

from lxml.etree import fromstring, tostring, SubElement, Element


class Mediapackage:

    namespaces = {
        '': 'http://mediapackage.opencastproject.org',
        'dcterms': 'http://purl.org/dc/terms/'
    }

    def __init__(self, mediapackage_xml):
        if mediapackage_xml is None:
            raise ValueError('Mediapackage XML is empty.')
        if isinstance(mediapackage_xml, bytes):
            self.__mediapackage = fromstring(mediapackage_xml)
        elif isinstance(mediapackage_xml, str):
            self.__mediapackage = fromstring(mediapackage_xml.encode('utf-8'))
        elif isinstance(mediapackage_xml, type(Element)):
            self.__mediapackage = fromstring(mediapackage_xml)
        else:
            raise TypeError('Unexpected Mediapackage format.')

    def __str__(self):
        return tostring(self.__mediapackage, pretty_print=True).decode('utf-8')

    def get_identifier(self):
        return self.__mediapackage.get('id')

    def get_title(self):
        return self.__mediapackage.findtext('title', namespaces=self.namespaces)

    def get_attachments(self, element_filter=lambda element: True):
        return [item for item in self.__get_elements('attachments/attachment', element_filter) or []]

    def get_catalogs(self, element_filter=lambda element: True):
        return [item for item in self.__get_elements('metadata/catalog', element_filter) or []]

    def get_tracks(self, element_filter=lambda element: True):
        return [item for item in self.__get_elements('media/track', element_filter) or []]

    def get_publications(self, element_filter=lambda element: True):
        return [item for item in self.__get_elements('publications/publication', element_filter) or []]

    def __get_elements(self, element_type, element_filter=lambda element: True):
        for element in filter(element_filter, self.__mediapackage.iterfind(f'./{element_type}', namespaces=self.namespaces)):
            yield MediapackageElement(element)

    def remove_element(self, element_filter=lambda element: False):
        for element in filter(element_filter, self.__mediapackage.iterfind('./attachments/attachment', namespaces=self.namespaces)):
            element.getparent().remove(element)
        for element in filter(element_filter, self.__mediapackage.iterfind('./media/track', namespaces=self.namespaces)):
            element.getparent().remove(element)
        for element in filter(element_filter, self.__mediapackage.iterfind('./metadata/catalog', namespaces=self.namespaces)):
            element.getparent().remove(element)
        for element in filter(element_filter, self.__mediapackage.iterfind('./publications/publication', namespaces=self.namespaces)):
            element.getparent().remove(element)

    def remove_publication(self, channel_id=None):
        """
        Removes publication with the given channel ID or if channel_id is None, all publication from the mediapackage.
        :param str channel_id:
            Publication channel identifier
        """
        publication_filter = lambda publication: not channel_id or publication.get('channel') == channel_id
        for element in filter(publication_filter, self.__mediapackage.iterfind('./publications/publication', namespaces=self.namespaces)):
            element.getparent().remove(element)

    def apply_tags(self, tags, element_filter=lambda element: True):
        append_tags, remove_tags, absolute_tags = self.__categorize_tags(tags)
        for element in filter(element_filter, self.__mediapackage.iterfind('./attachments/attachment', namespaces=self.namespaces)):
            self.__apply_tags_on_element(element, append_tags, remove_tags, absolute_tags)
        for element in filter(element_filter, self.__mediapackage.iterfind('./media/track', namespaces=self.namespaces)):
            self.__apply_tags_on_element(element, append_tags, remove_tags, absolute_tags)
        for element in filter(element_filter, self.__mediapackage.iterfind('./metadata/catalog', namespaces=self.namespaces)):
            self.__apply_tags_on_element(element, append_tags, remove_tags, absolute_tags)
        for element in filter(element_filter, self.__mediapackage.iterfind('./publications/publication', namespaces=self.namespaces)):
            self.__apply_tags_on_element(element, append_tags, remove_tags, absolute_tags)

    @staticmethod
    def __categorize_tags(tags):
        append_tags = []
        remove_tags = []
        absolute_tags = []
        for tag in tags or []:
            if not tag:
                continue
            if tag[0] == '+':
                if absolute_tags:
                    raise ValueError('Can\'t apply append and absolute tags at the same time.')
                append_tags.append(tag[1:])
            elif tag[0] == '-':
                if absolute_tags:
                    raise ValueError('Can\'t apply remove and absolute tags at the same time.')
                remove_tags.append(tag[1:])
            else:
                if append_tags or remove_tags:
                    raise ValueError('Can\'t apply relative and absolute tags at the same time.')
                absolute_tags.append(tag)
        for tag in list(set(append_tags) & set(remove_tags)) or list():
            append_tags.remove(tag)
            remove_tags.remove(tag)
        append_tags = list(set(append_tags))
        remove_tags = list(set(remove_tags))
        return append_tags, remove_tags, absolute_tags

    def __apply_tags_on_element(self, element, append_tags, remove_tags, absolute_tags):
        element_tags = [tag_element.text for tag_element in element.findall('./tags/tag', namespaces=self.namespaces)]
        if absolute_tags:
            for tag_element in element.iterfind('./tags/tag', namespaces=self.namespaces):
                if tag_element.text in absolute_tags:
                    continue
                tag_element.getparent().remove(tag_element)
            tags_element = element.find('./tags', namespaces=self.namespaces)
            for tag in absolute_tags:
                if tag not in element_tags:
                    tag_element = SubElement(tags_element, tags_element.tag[:-1])
                    tag_element.text = tag
        else:
            tags_element = element.find('./tags', namespaces=self.namespaces)
            for tag in list(set(remove_tags) & set(element_tags)):
                for tag_element in tags_element.findall('./tag', namespaces=self.namespaces):
                    # lxml does not support xpath check text() like './/tag[text()="tagname"]'
                    if tag_element.text == tag:
                        tag_element.getparent().remove(tag_element)
            for tag in append_tags:
                if tag not in element_tags:
                    tag_element = SubElement(tags_element, tags_element.tag[:-1])
                    tag_element.text = tag

    def merge(self, other, element_filter=lambda element: True):
        attachments_element = self.__mediapackage.find('./attachments', namespaces=self.namespaces)
        media_element = self.__mediapackage.find('./media', namespaces=self.namespaces)
        metadata_element = self.__mediapackage.find('./metadata', namespaces=self.namespaces)
        publications_element = self.__mediapackage.find('./publications', namespaces=self.namespaces)
        for element in filter(element_filter, other.__mediapackage.iterfind('./attachments/attachment', namespaces=self.namespaces)):
            attachments_element.append(element)
        for element in filter(element_filter, other.__mediapackage.iterfind('./media/track', namespaces=self.namespaces)):
            media_element.append(element)
        for element in filter(element_filter, other.__mediapackage.iterfind('./metadata/catalog', namespaces=self.namespaces)):
            metadata_element.append(element)
        for element in filter(element_filter, other.__mediapackage.iterfind('./publications/publication', namespaces=self.namespaces)):
            publications_element.append(element)

    def add_attachment(self, flavor, url, element_id=None, ref=None, tags=[]):
        self.__add_element('attachment', flavor, url, element_id or str(uuid1()), ref, tags)

    def add_catalog(self, flavor, url, element_id=None, ref=None, tags=[]):
        self.__add_element('catalog', flavor, url, element_id or str(uuid1()), ref, tags)

    def add_track(self, flavor, url, element_id=None, ref=None, tags=[]):
        self.__add_element('track', flavor, url, element_id or str(uuid1()), ref, tags)

    def __add_element(self, element_type, flavor, url, element_id, ref=None, tags=[]):
        if element_type == 'attachment':
            container = self.__mediapackage.find('./attachments', namespaces=self.namespaces)
            if container is None:
                container = SubElement(self.__mediapackage, '{http://mediapackage.opencastproject.org}attachments')
            element = SubElement(container, '{http://mediapackage.opencastproject.org}attachment')
        elif element_type == 'catalog':
            container = self.__mediapackage.find('./metadata', namespaces=self.namespaces)
            if container is None:
                container = SubElement(self.__mediapackage, '{http://mediapackage.opencastproject.org}metadata')
            element = SubElement(container, '{http://mediapackage.opencastproject.org}catalog')
        elif element_type == 'track':
            container = self.__mediapackage.find('./media', namespaces=self.namespaces)
            if container is None:
                container = SubElement(self.__mediapackage, '{http://mediapackage.opencastproject.org}media')
            element = SubElement(container, '{http://mediapackage.opencastproject.org}track')
        else:
            raise ValueError(f'Element type must be "attachment", "catalog" or "track" but is {element_type}.')
        element.attrib['id'] = element_id
        if flavor:
            element.attrib['type'] = flavor
        if ref:
            element.attrib['ref'] = ref
        url_element = SubElement(element, '{http://mediapackage.opencastproject.org}url')
        url_element.text = url
        if tags:
            tags_element = SubElement(element, '{http://mediapackage.opencastproject.org}tags')
            for tag in tags:
                if not tag:
                    continue
                tag_element = SubElement(tags_element, '{http://mediapackage.opencastproject.org}tag')
                tag_element.text = tag if tag[:1] not in ['+', '-'] else tag[1:]

    def add_elements_from_publication(self, publication_channel, element_filter=lambda element: True, tags=[]):
        append_tags, remove_tags, absolute_tags = self.__categorize_tags(tags)
        added_elements = list()
        publication_filter = lambda e: 'channel' in e.keys() and e.get('channel') == publication_channel
        for publication_element in filter(publication_filter,
                                          self.__mediapackage.iterfind('./publications/publication',
                                                                       namespaces=self.namespaces)):
            assert publication_element.tag == '{http://mediapackage.opencastproject.org}publication'
            assert publication_element.get('channel', None) == publication_channel
            for element in filter(element_filter, publication_element.iterfind('./attachments/attachment',
                                                                                namespaces=self.namespaces)):
                assert element.tag == '{http://mediapackage.opencastproject.org}attachment'
                new_element = deepcopy(element)
                self.__apply_tags_on_element(new_element, append_tags, remove_tags, absolute_tags)
                container = self.__mediapackage.find('./attachments', namespaces=self.namespaces)
                if container is None:
                    container = SubElement(self.__mediapackage, '{http://mediapackage.opencastproject.org}attachments')
                container.append(new_element)
                added_elements.append(MediapackageElement(new_element))
            for element in filter(element_filter, publication_element.iterfind('./media/track',
                                                                                namespaces=self.namespaces)):
                assert element.tag == '{http://mediapackage.opencastproject.org}track'
                new_element = deepcopy(element)
                self.__apply_tags_on_element(new_element, append_tags, remove_tags, absolute_tags)
                container = self.__mediapackage.find('./media', namespaces=self.namespaces)
                if container is None:
                    container = SubElement(self.__mediapackage, '{http://mediapackage.opencastproject.org}media')
                container.append(new_element)
                added_elements.append(MediapackageElement(new_element))
            for element in filter(element_filter, publication_element.iterfind('./metadata/catalog',
                                                                                namespaces=self.namespaces)):
                assert element.tag == '{http://mediapackage.opencastproject.org}catalog'
                new_element = deepcopy(element)
                self.__apply_tags_on_element(new_element, append_tags, remove_tags, absolute_tags)
                container = self.__mediapackage.find('./metadata', namespaces=self.namespaces)
                if container is None:
                    container = SubElement(self.__mediapackage, '{http://mediapackage.opencastproject.org}metadata')
                container.append(new_element)
                added_elements.append(MediapackageElement(new_element))
        return added_elements


class MediapackageElement:

    namespaces = {
        '': 'http://mediapackage.opencastproject.org',
        'dcterms': 'http://purl.org/dc/terms/'
    }

    def __init__(self, element):
        self.__element = element

    def __str__(self):
        return tostring(self.__element, pretty_print=True).decode('utf-8')

    def _get_xml_element(self):
        return self.__element

    def get_identifier(self):
        return self.__element.get('id')

    def get_flavor(self):
        return self.__element.get('type')

    def get_tags(self):
        return [tag_element.text for tag_element in self.__element.findall('./tags/tag', namespaces=self.namespaces)
                if tag_element.text is not None]

    def get_references(self):
        return self.__element.get('ref')

    def get_url(self):
        return self.__element.findtext('./url', namespaces=self.namespaces)

    def get_attr(self, name):
        return self.__element.get(name)

class PublicationMediapackageElement(MediapackageElement):

    def __init__(self, element:MediapackageElement):
        super().__init__(element._get_xml_element())

    def get_channel(self):
        return self._get_xml_element().get('channel')

    def get_mimetype(self):
        return self._get_xml_element().findtext('./mimetype', namespaces=self.namespaces)

    def get_attachments(self, element_filter=lambda element: True):
        return [item for item in self.__get_elements('attachments/attachment', element_filter) or []]

    def get_catalogs(self, element_filter=lambda element: True):
        return [item for item in self.__get_elements('metadata/catalog', element_filter) or []]

    def get_tracks(self, element_filter=lambda element: True):
        return [item for item in self.__get_elements('media/track', element_filter) or []]

    def get_publications(self, element_filter=lambda element: True):
        return [item for item in self.__get_elements('publications/publication', element_filter) or []]

    def __get_elements(self, element_type, element_filter=lambda element: True):
        for element in filter(element_filter, self._get_xml_element().iterfind(f'./{element_type}', namespaces=self.namespaces)):
            yield MediapackageElement(element)