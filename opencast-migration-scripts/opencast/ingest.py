#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import makedirs, walk, remove, rmdir, rename
from os.path import isdir, abspath, join, isfile, relpath
from urllib.parse import urlparse, quote
from zipfile import ZipFile

from httpx import Timeout, Client, URL

import opencast


def xml_escape_url(url: str) -> str:
    if url is None:
        return url
    url_split = url.split('?', 1)
    if len(url_split) > 1:
        url_params = url_split[1]
        url_params = url_params.replace("&", "&amp;")
        url_params = url_params.replace("<", "&lt;")
        url_params = url_params.replace(">", "&gt;")
        url_params = url_params.replace('"', "&quot;")
        url_params = url_params.replace("'", "&apos;")
        return '?'.join([url_split[0], url_params])
    return url_split[0]


def ingest_zipped_mediapackage(source_opencast_admin_client, source_opencast_presentation_client,
                               target_opencast_admin_client, mediapackage,
                               workflow_definition_id='', workflow_properties=dict(),
                               tmp_dir=opencast.tmp_dir):
    assert(source_opencast_admin_client)
    assert(source_opencast_presentation_client)
    assert(target_opencast_admin_client)
    assert(mediapackage)
    manifest = str(mediapackage)
    mediapackage_id = mediapackage.get_identifier()
    assert(mediapackage_id)
    zip_filepath = abspath(join(tmp_dir, mediapackage_id + '.zip'))
    try:
        # download elements and update urls in media package
        for catalog in mediapackage.get_catalogs():
            filepath, filesize = download_mediapackage_element(
                source_opencast_admin_client, source_opencast_presentation_client,
                mediapackage_id, catalog, tmp_dir=tmp_dir)
            if filepath and filesize <= 0:
                print(f'WARNING: The downloaded file {filepath} is empty. Skip processing file.')
                remove(filepath)
            else:
                manifest = manifest.replace(
                    xml_escape_url(catalog.get_url()),
                    relpath(filepath, abspath(join(tmp_dir, mediapackage_id))))
        for attachment in mediapackage.get_attachments():
            filepath, filesize = download_mediapackage_element(
                source_opencast_admin_client, source_opencast_presentation_client,
                mediapackage_id, attachment, tmp_dir=tmp_dir)
            if filepath and filesize <= 0:
                print(f'WARNING: The downloaded file {filepath} is empty. Skip processing file.')
                remove(filepath)
            else:
                manifest = manifest.replace(
                    xml_escape_url(attachment.get_url()),
                    relpath(filepath, abspath(join(tmp_dir, mediapackage_id))))
        for track in mediapackage.get_tracks():
            filepath, filesize = download_mediapackage_element(
                source_opencast_admin_client, source_opencast_presentation_client,
                mediapackage_id, track, tmp_dir=tmp_dir)
            if filepath and filesize <= 0:
                print(f'WARNING: The downloaded file {filepath} is empty. Skip processing file.')
                remove(filepath)
            else:
                manifest = manifest.replace(
                    xml_escape_url(track.get_url()),
                    relpath(filepath, abspath(join(tmp_dir, mediapackage_id))))
        # write manifest
        with open(join(tmp_dir, mediapackage_id, 'manifest.xml'), 'w', encoding='UTF-8') as manifest_file:
            manifest_file.write(manifest)
        # zip media package
        print(f'Zip media package {mediapackage_id}')
        with ZipFile(zip_filepath, 'w') as zipfile:
            for d, _, fl in walk(join(tmp_dir, mediapackage_id)):
                for f in fl:
                    arcname = join(relpath(d, tmp_dir), f)
                    zipfile.write(join(d, f), arcname=arcname)
        # upload zip file
        url = f'/ingest/addZippedMediaPackage/{workflow_definition_id}'
        params = []
        for k, v in workflow_properties.items():
            if k == 'workflowDefinitionId' and workflow_definition_id:
                # do not pass workflow definition ID as argument if we want to set it explicitly
                continue
            params.append((k, (None, v.encode('utf-8'))))
        params.append(('BODY', (join(mediapackage_id + '.zip'), open(zip_filepath, 'rb'))))
        print(f'Ingest zipped media package {mediapackage_id} and start workflow {workflow_definition_id}.')
        result = target_opencast_admin_client.post(url, files=params, timeout=Timeout(600))
        result.raise_for_status()
        return result.text
    finally:
        remove_mediapackage_tmp_dir(mediapackage_id, tmp_dir=tmp_dir)
        if isfile(zip_filepath):
            remove(zip_filepath)


def download_mediapackage_element(source_opencast_admin_client, source_opencast_presentation_client,
                                  mediapackage_id, mediapackage_element, tmp_dir=opencast.tmp_dir):
    assert mediapackage_id
    element_filename = filename_from_url(mediapackage_element.get_url())
    assert element_filename
    element_filepath, filesize = download_file(
        source_opencast_admin_client, source_opencast_presentation_client,
        mediapackage_element.get_url(),
        subdir=join(mediapackage_id, mediapackage_element.get_identifier()),
        filename=get_filename_prefix(mediapackage_element) + element_filename,
        tmp_dir=tmp_dir)
    assert element_filepath
    if element_filepath.endswith('.unknown'):
        # parse mimetype
        import magic
        mimetype = magic.from_file(element_filepath, mime=True)
        import mimetypes
        mimetype_file_ext = mimetypes.guess_extension(mimetype, strict=False)
        if mimetype_file_ext is not None:
            print(f'Fix filename extension for {element_filepath} '
                  f'based on file mimtype {mimetype}: {mimetype_file_ext[1:]}')
            new_element_filepath = f'{element_filepath.removesuffix(".unknown")}{mimetype_file_ext}'
            rename(src=element_filepath, dst=new_element_filepath)
            element_filepath = new_element_filepath
    return element_filepath, filesize


def ingest_mediapackage(source_opencast_admin_client, source_opencast_presentation_client,
                        target_opencast_admin_client, mediapackage,
                        workflow_definition_id='', workflow_properties=dict(),
                        tmp_dir=opencast.tmp_dir):
    url = f'/ingest/createMediaPackageWithID/{mediapackage.get_identifier()}'
    result = target_opencast_admin_client.put(url)
    result.raise_for_status()
    result_mediapackage_xml = result.text

    try:
        # ingest catalogs
        for catalog in mediapackage.get_catalogs():
            result_mediapackage_xml = ingest_mediapackage_element(
                source_opencast_admin_client, source_opencast_presentation_client,
                target_opencast_admin_client,
                result_mediapackage_xml, mediapackage.get_identifier(),
                catalog, 'catalog',
                tmp_dir)

        # ingest attachments
        for attachment in mediapackage.get_attachments():
            result_mediapackage_xml = ingest_mediapackage_element(
                source_opencast_admin_client, source_opencast_presentation_client,
                target_opencast_admin_client,
                result_mediapackage_xml, mediapackage.get_identifier(),
                attachment, 'attachment',
                tmp_dir)

        # ingest tracks
        for track in mediapackage.get_tracks():
            result_mediapackage_xml = ingest_mediapackage_element(
                source_opencast_admin_client, source_opencast_presentation_client,
                target_opencast_admin_client,
                result_mediapackage_xml, mediapackage.get_identifier(),
                track, 'track',
                tmp_dir)

        url = f'/ingest/ingest/{workflow_definition_id}'
        params = [
            ('mediaPackage', (None, result_mediapackage_xml.encode('utf-8'), 'text/xml')),
        ]
        for k, v in workflow_properties.items():
            params.append((k, (None, v.encode('utf-8'))))
        print(f'Start workflow {workflow_definition_id} on media package {mediapackage.get_identifier()}.')
        result = target_opencast_admin_client.post(url, files=params, timeout=Timeout(600))
        result.raise_for_status()
        return result.text
    finally:
        remove_mediapackage_tmp_dir(mediapackage.get_identifier(), tmp_dir)


def schedule_mediapackage(source_opencast_admin_client, source_opencast_presentation_client,
                          target_opencast_admin_client, mediapackage,
                          workflow_definition_id='', workflow_properties=dict(),
                          tmp_dir=opencast.tmp_dir):
    url = f'/ingest/createMediaPackageWithID/{mediapackage.get_identifier()}'
    result = target_opencast_admin_client.put(url)
    result.raise_for_status()
    result_mediapackage_xml = result.text

    try:
        # ingest catalogs
        for catalog in mediapackage.get_catalogs():
            result_mediapackage_xml = ingest_mediapackage_element(
                source_opencast_admin_client, source_opencast_presentation_client,
                target_opencast_admin_client,
                result_mediapackage_xml, mediapackage.get_identifier(),
                catalog, 'catalog',
                tmp_dir)

        # ingest attachments
        for attachment in mediapackage.get_attachments():
            result_mediapackage_xml = ingest_mediapackage_element(
                source_opencast_admin_client, source_opencast_presentation_client,
                target_opencast_admin_client,
                result_mediapackage_xml, mediapackage.get_identifier(),
                attachment, 'attachment',
                tmp_dir)

        url = f'/ingest/schedule/{workflow_definition_id}'
        params = [
            ('mediaPackage', (None, quote(result_mediapackage_xml).encode('utf-8'), 'text/xml')),
        ]
        for k, v in workflow_properties.items():
            params.append((k, (None, v.encode('utf-8'))))
        print(f'Create schedule for media package {mediapackage.get_identifier()}.')
        result = target_opencast_admin_client.post(url, files=params, timeout=Timeout(600))
        result.raise_for_status()
    finally:
        remove_mediapackage_tmp_dir(mediapackage.get_identifier())


def ingest_mediapackage_element(source_opencast_admin_client, source_opencast_presentation_client,
                                target_opencast_admin_client,
                                mediapackage_xml, mediapackage_id,
                                mediapackage_element, element_type,
                                tmp_dir):
    assert(mediapackage_xml)
    assert(mediapackage_element.get_identifier())
    if not mediapackage_element.get_url():
        print(f'Element {mediapackage_element.get_flavor()} with ID {mediapackage_element.get_identifier()} '
              f'of type {element_type} from media package {mediapackage_id} does not set url. Skip processing.')
        return mediapackage_xml
    if element_type.lower() == 'attachment':
        url = '/ingest/addAttachment'
    elif element_type.lower() == 'catalog':
        url = '/ingest/addCatalog'
    elif element_type.lower() == 'track':
        url = '/ingest/addTrack'
        if is_streaming_url(mediapackage_element.get_url()):
            print(f'Skip download streaming URL {str(mediapackage_element.get_url())}')
            return mediapackage_xml
    else:
        raise ValueError(f'Element type must be \'attachment\', \'catalog\' or \'track\' but is \'{element_type}\'.')
    element_filename = filename_from_url(mediapackage_element.get_url())
    assert(element_filename)
    element_filepath, _ = download_file(source_opencast_admin_client, source_opencast_presentation_client,
                                        mediapackage_element.get_url(),
                                        subdir=join(mediapackage_id, mediapackage_element.get_identifier()),
                                        filename=get_filename_prefix(mediapackage_element) + element_filename,
                                        tmp_dir=tmp_dir)
    params = [
        ('flavor', (None, mediapackage_element.get_flavor().encode('utf-8'))),
        ('tags', (None, ','.join(mediapackage_element.get_tags()).encode('utf-8'))),
        ('mediaPackage', (None, mediapackage_xml.encode('utf-8'), 'text/xml')),
        ('BODY', (element_filename, open(element_filepath, 'rb'))),
    ]
    print(f'Upload file {element_filepath} as {element_type}')
    result = target_opencast_admin_client.post(url, files=params)
    remove(element_filepath)
    result.raise_for_status()
    return result.text


def remove_mediapackage_tmp_dir(mediapackage_id, tmp_dir=opencast.tmp_dir):
    dir_path = abspath(join(tmp_dir, mediapackage_id))
    if not isdir(dir_path):
        return
    deleteFiles = []
    deleteDirs = []
    for root, dirs, files in walk(dir_path):
        for f in files:
            deleteFiles.append(join(root, f))
        for d in dirs:
            deleteDirs.append(join(root, d))
    for f in deleteFiles:
        remove(f)
    for d in deleteDirs:
        rmdir(d)
    rmdir(dir_path)


def get_filename_prefix(mediapackage_element):
    if 'search' in mediapackage_element.get_tags():
        return 'search_'
    elif 'internal' in mediapackage_element.get_tags():
        return 'internal_'
    else:
        return 'archive_'


def filename_from_url(url):
    if not url:
        return url
    result = url.split('?')[0]
    return result.split('/')[-1]


def is_streaming_url(file_url):
    url = urlparse(file_url)
    return url.scheme in ['rtp', 'rtmp'] or \
           url.path.endswith('.m3u8') or \
           url.path.endswith('.mpd') or \
           url.path.endswith('.f4m') or \
           url.path.endswith('/Manifest')


def download_file(opencast_admin_client, opencast_presentation_client, url, subdir, filename, tmp_dir=opencast.tmp_dir):
    output_dir = abspath(join(abspath(tmp_dir), subdir))
    if not output_dir.startswith(abspath(tmp_dir)):
        raise ValueError(f'Output directory ({output_dir}) is not part of working directory ({abspath(tmp_dir)})')
    if not isdir(output_dir):
        makedirs(output_dir, exist_ok=True)

    output_path = join(output_dir, filename)
    if isfile(output_path):
        print(f'File {output_path} exists. Skip download.')
        return output_path, -1
    print(f'Download file {url} to {output_path}')
    download_url = urlparse(url)
    if opencast_admin_client.base_url.host == download_url.hostname or \
            (download_url.hostname == 'localhost' and download_url.port == 8080):
        print('Using Opencast Admin HTTP client')
        opencast_client = opencast_admin_client
    elif opencast_presentation_client.base_url.host == download_url.hostname:
        print('Using Opencast Presentation HTTP client')
        opencast_client = opencast_presentation_client
    else:
        print('Using new HTTP client')
        opencast_client = Client()

    def stream_to_file(stream_output_file, stream_response):
        _bytes_written = 0
        for chunk in stream_response.iter_bytes(chunk_size=1024 * 1024 * 100):  # chunk size 100MB
            _bytes_written += stream_output_file.write(chunk)
        return _bytes_written

    bytes_written = 0
    with open(output_path, mode='wb') as output_file:
        redirect_url = None
        stream_url = download_url.path
        if download_url.query:
            stream_url += f'?{download_url.query}'
        with opencast_client.stream('GET', url=stream_url) as response:
            if response.status_code == 302 and response.next_request.url and \
                    response.next_request.url.path == URL(url).path:
                # redirect to download distribution host
                # download distribution nodes do not implement authentication, let's assure
                redirect_url = response.next_request.url.copy_with(username="", password="")
            else:
                response.raise_for_status()
                bytes_written = stream_to_file(output_file, response)
        if redirect_url and bytes_written == 0:
            import httpx
            print(f'Follow redirect to URL: {redirect_url}')
            with httpx.stream('GET', url=redirect_url, timeout=opencast_client.timeout) as response:
                response.raise_for_status()
                bytes_written = stream_to_file(output_file, response)
    return output_path, bytes_written
