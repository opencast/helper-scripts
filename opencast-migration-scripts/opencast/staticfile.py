#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import unlink, mkdir
from os.path import join, abspath, isfile, isdir


def reupload_static_file(source_opencast_presentation_client, target_opencast_presentation_client,
                         file_url, filename, tmp_dir, file_id):
    try:
        download_static_file(source_opencast_presentation_client, file_url, tmp_dir, file_id)
        target_filename = upload_static_file(target_opencast_presentation_client, filename, tmp_dir, file_id)
        unlink(join(abspath(tmp_dir), file_id))
        return target_filename
    except Exception as e:
        if isfile(join(abspath(tmp_dir), filename)):
            unlink(join(abspath(tmp_dir), filename))
        raise e


def download_static_file(opencast_presentation_client, file_url, tmp_dir, file_id):
    if tmp_dir and not isdir(abspath(tmp_dir)):
        mkdir(abspath(tmp_dir))

    output_path = join(abspath(tmp_dir), file_id)
    if isfile(output_path):
        print(f'File "{output_path}" exists. Skip download.')
        return
    with open(output_path, mode='wb') as output_file:
        with opencast_presentation_client.stream('GET', url=file_url) as response:
            for chunk in response.iter_bytes(chunk_size=1024*1024*10):   # chunk size 10MB
                output_file.write(chunk)


def upload_static_file(opencast_presentation_client, filename, tmp_dir, file_id):
    url = '/staticfiles'
    source_file_path = join(abspath(tmp_dir), file_id)
    files = {'BODY': (filename, open(source_file_path, 'rb'))}
    response = opencast_presentation_client.post(url, files=files)
    response.raise_for_status()
    return response.text
