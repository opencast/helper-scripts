#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from opencast.staticfile import reupload_static_file


def get_themes(opencast_admin_client):
    url = '/admin-ng/themes/themes.json'
    offset = 0
    batch_size = 20
    while offset >= 0:
        params = {
            'limit': batch_size,
            'offset': offset,
            'sort': 'creation_date:ASC',
        }
        response = opencast_admin_client.get(url, params=params)
        response.raise_for_status()
        items = response.json().get('results') if response.json() and response.json().get('results') else []
        for theme_item in items:
            yield theme_item
        if items:
            offset += batch_size
        else:
            offset = -1
            if offset == 0:
                return []


def get_theme(opencast_admin_client, theme_id):
    url = f'/admin-ng/themes/{theme_id}.json'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    return response.json()


def create_theme(target_opencast_admin_client, target_opencast_presentation_client,
                 source_opencast_admin_client, source_opencast_presentation_client,
                 theme_id: str, tmp_dir: str):
    theme = get_theme(source_opencast_admin_client, theme_id)
    theme_metadata = dict(theme)
    print(f'Create theme \'{theme_metadata["name"]}\' (ID: {theme_id})')
    if 'bumperFile' in theme and theme['bumperFile']:
        print(f'Upload theme bumper file '
              f'{theme["bumperFile"]} for theme \'{theme_metadata["name"]}\' (ID: {theme_id}).')
        target_filename = reupload_static_file(
            source_opencast_presentation_client=source_opencast_presentation_client,
            target_opencast_presentation_client=target_opencast_presentation_client,
            file_url=theme['bumperFileUrl'], filename=theme['bumperFileName'],
            tmp_dir=tmp_dir, file_id=theme["bumperFile"])
        print(f'Theme bumper file {theme["bumperFile"]} uploaded as {target_filename}')
        theme_metadata['bumperFile'] = target_filename
        del theme_metadata['bumperFileUrl']
        del theme_metadata['bumperFileName']
    if 'titleSlideBackground' in theme and theme['titleSlideBackground']:
        print(f'Upload theme title slide background file '
              f'{theme["titleSlideBackground"]} for theme \'{theme_metadata["name"]}\' (ID: {theme_id}).')
        target_filename = reupload_static_file(
            source_opencast_presentation_client=source_opencast_presentation_client,
            target_opencast_presentation_client=target_opencast_presentation_client,
            file_url=theme['titleSlideBackgroundUrl'], filename=theme['titleSlideBackgroundName'],
            tmp_dir=tmp_dir, file_id=theme["titleSlideBackground"])
        print(f'Theme title slide background file {theme["titleSlideBackground"]} uploaded as {target_filename}')
        theme_metadata['titleSlideBackground'] = target_filename
        del theme_metadata['titleSlideBackgroundUrl']
        del theme_metadata['titleSlideBackgroundName']
    if 'trailerFile' in theme and theme['trailerFile']:
        print(f'Upload theme trailer file '
              f'{theme["trailerFile"]} for theme \'{theme_metadata["name"]}\' (ID: {theme_id}).')
        target_filename = reupload_static_file(
            source_opencast_presentation_client=source_opencast_presentation_client,
            target_opencast_presentation_client=target_opencast_presentation_client,
            file_url=theme['trailerFileUrl'], filename=theme['trailerFileName'],
            tmp_dir=tmp_dir, file_id=theme["trailerFile"])
        print(f'Theme trailer file {theme["trailerFile"]} uploaded as {target_filename}')
        theme_metadata['trailerFile'] = target_filename
        del theme_metadata['trailerFileUrl']
        del theme_metadata['trailerFileName']
    if 'watermarkFile' in theme and theme['watermarkFile']:
        print(f'Upload theme watermark file '
              f'{theme["watermarkFile"]} for theme \'{theme_metadata["name"]}\' (ID: {theme_id}).')
        target_filename = reupload_static_file(
            source_opencast_presentation_client=source_opencast_presentation_client,
            target_opencast_presentation_client=target_opencast_presentation_client,
            file_url=theme['watermarkFileUrl'], filename=theme['watermarkFileName'],
            tmp_dir=tmp_dir, file_id=theme["watermarkFile"])
        print(f'Theme watermark file {theme["watermarkFile"]} uploaded as {target_filename}')
        theme_metadata['watermarkFile'] = target_filename
        del theme_metadata['watermarkFileUrl']
        del theme_metadata['watermarkFileName']
    url = '/admin-ng/themes/'
    response = target_opencast_admin_client.post(url, data=theme_metadata)
    response.raise_for_status()
    created_theme = response.json()
    print(f'Created theme \'{created_theme.get("name", "UNKNOWN NAME")}\' '
          f'(ID: {created_theme.get("id", "MISSING ID")} from theme ID: {theme_id})')
    return created_theme


def append_editor_previews(opencast_admin_client, mediapackage, tags=[]):
    url = f'/admin-ng/tools/{mediapackage.get_identifier()}/editor.json'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    editor_json = response.json()
    if not editor_json:
        return
    preview_track_types = list()
    for editor_track in editor_json.get('tracks', []):
        track_flavor = editor_track.get('flavor', None)
        preview_track_types.append(track_flavor)
        track_waveform = editor_track.get('waveform', None)
        track_id = editor_track.get('id', None)
        if track_flavor and track_waveform:
            mediapackage.add_attachment(f'{track_flavor}/waveform', track_waveform, element_id=track_id, tags=tags)

    for preview_track in editor_json.get('previews', []):
        if 'uri' not in preview_track:
            continue
        preview_track_flavor_type = preview_track_types[0] if len(preview_track_types) == 1 else 'composite'
        mediapackage.add_track(f'{preview_track_flavor_type}/preview', preview_track['uri'], tags=tags)

    for source_track in editor_json.get('source_tracks', []):
        if 'flavor' not in source_track and not ('audio' in source_track or 'video' in source_track):
            continue
        if 'audio' in source_track:
            preview_image = source_track.get('audio').get('preview_image')
            if preview_image:
                preview_flavor = f'{source_track.get("flavor").get("type")}/audio+preview'
                mediapackage.add_attachment(preview_flavor, preview_image, tags=tags)
        if 'video' in source_track:
            preview_image = source_track.get('video').get('preview_image')
            if preview_image:
                preview_flavor = f'{source_track.get("flavor").get("type")}/video+preview'
                mediapackage.add_attachment(preview_flavor, preview_image, tags=tags)
