# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                     Version 2, December 2004
#
#  Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
#  Everyone is permitted to copy and distribute verbatim or modified
#  copies of this license document, and changing it is allowed as long
#  as the name is changed.
#
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#   0. You just DO WHAT THE FUCK YOU WANT TO.

# requires: python-requests, python-jinja2

import ConfigParser
import datetime
from jinja2 import Environment, FileSystemLoader
import logging
import os
import random
import requests
from requests.auth import HTTPDigestAuth
import shutil
import uuid

LOG_LEVEL = logging.INFO
EVENT_SOURCE='simulated:opencast-simulate-ingests:'
INGEST_ENDPOINT = '/ingest/addZippedMediaPackage/'
MEDIAPACKAGE_DIR = 'mediapackages/'
TEMPLATE_DIR = MEDIAPACKAGE_DIR + 'templates/'
TRACK_DIR = MEDIAPACKAGE_DIR + 'tracks/'
TMP_DIR = MEDIAPACKAGE_DIR + 'tmp/'
ZIP_DIR = MEDIAPACKAGE_DIR + 'zips/'


def get_config_section(config, section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            value = config.get(section, option)
            try:
                dict1[option] = int(value)
            except:
                try:
                    dict1[option] = float(value)
                except:
                    dict1[option] = value
            if dict1[option] == -1:
                print('skip: %s' % option)
        except:
            print('exception on %s!' % option)
            dict1[option] = None
    return dict1


def get_profile(index):
    prefix = 'profile.{0}.'.format(index)
    return {
        'type': Mediapackages[prefix + 'type'],
        'duration': Mediapackages[prefix + 'duration'],
        'freq': Mediapackages[prefix + 'freq'],
        'video.presentation': Mediapackages[prefix + 'video.presentation'],
        'video.presenter': Mediapackages[prefix + 'video.presenter'],
        'audio.presentation': Mediapackages[prefix + 'audio.presentation'],
        'audio.presenter': Mediapackages[prefix + 'audio.presenter'],
        'video.ext': Mediapackages[prefix + 'video.ext'] if prefix + 'video.ext' in Mediapackages else 'avi',
        'audio.ext': Mediapackages[prefix + 'audio.ext'] if prefix + 'audio.ext' in Mediapackages else 'mp3',
    }


def create_mediapackage(profile):
    mime = dict(avi='msvideo', mp4='mp4', mov='quicktime', mp3='mp3')
    
    # create tmp workspace
    mp_id = unicode(uuid.uuid4())
    mp_dir = TMP_DIR + mp_id + '/'
    os.makedirs(mp_dir)

    try:
        duration = profile['duration']
        if duration >= 1:
            duration_ms = int((55 + 60*(duration-1))*60000)
        else:
            duration_ms = int(duration*3600000)

        # Edit the episode.xml and manifest.xml datetime params
        now = datetime.datetime.utcnow()
        today = now.strftime('%Y-%m-%d')
        delta = datetime.timedelta(milliseconds=duration_ms)
        iso_datetime = (now-delta).strftime('%Y-%m-%dT%H:%M:%SZ')

        # Create series xml unique per day
        series_title = 'Simulated Ingests ' + today
        series_id = uuid.uuid3(uuid.NAMESPACE_URL, "{0}{1}".format(Opencast['admin'], today))
        series_vars = dict(identifier=series_id, created=today + 'T00:00:00Z', title=series_title, source=EVENT_SOURCE)
        series_template = Templates.get_template('series.xml')
        series_template.stream(series_vars).dump(mp_dir + 'series.xml')
        log.debug('series id {0} title {1}'.format(series_id, series_title))

        # Create episode xml
        location = os.uname()[1]  # nodename
        title = 'Test Recording from {0} - {1}'.format(location, iso_datetime)
        ep_vars = dict(identifier=mp_id, created=iso_datetime, title=title, source=EVENT_SOURCE, spatial=location,
                       is_part_of=series_id)
        ep_template = Templates.get_template('episode.xml')
        ep_template.stream(ep_vars).dump(mp_dir + 'episode.xml')
        log.debug('mediapackage id {0} title {1}'.format(mp_id, title))

        # Create manifest/mediapackage xml
        type = profile['type']
        video_ext = profile['video.ext']
        audio_ext = profile['audio.ext']
        mp_vars = dict(indentifer=mp_id, created=iso_datetime, duration=duration_ms,
                       title=title, series_title=series_title,
                       has_presentation_video=profile['video.presentation'] == 'True',
                       has_presenter_video=profile['video.presenter'] == 'True',
                       has_presentation_audio=profile['audio.presentation'] == 'True',
                       has_presenter_audio=profile['audio.presenter'] == 'True',
                       video_ext=video_ext, audio_ext=audio_ext, video_mime=mime[video_ext], audio_mime=mime[audio_ext])
        mp_template = Templates.get_template('manifest.xml')
        mp_template.stream(mp_vars).dump(mp_dir + 'manifest.xml')

        # Create capture agent properties, largely btw as superceded by POST parameters
        edit = False
        publish = Ingest['publish']

        ca_vars = dict(location=location, title=title, series_id=series_id, email=Ingest['email'],
                       workflow=Ingest['workflow'], edit=edit, publish=publish)
        ca_template = Templates.get_template('org.opencastproject.capture.agent.properties')
        ca_template.stream(ca_vars).dump(mp_dir + 'org.opencastproject.capture.agent.properties')

        # Copy tracks
        if mp_vars['has_presentation_video']:
            track = 'presentation-{0}-{1}.{2}'.format(type, duration, video_ext)
            os.link(TRACK_DIR + track, mp_dir + 'presentation.' + video_ext)
        if mp_vars['has_presenter_video']:
            track = 'presenter-{0}-{1}.{2}'.format(type, duration, video_ext)
            os.link(TRACK_DIR + track, mp_dir + 'presenter.' + video_ext)
        if mp_vars['has_presentation_audio']:
            track = 'presentation-{0}-{1}.{2}'.format(type, duration, audio_ext)
            os.link(TRACK_DIR + track, mp_dir + 'presentation.' + audio_ext)
        if mp_vars['has_presenter_audio']:
            track = 'presenter-{0}-{1}.{2}'.format(type, duration, audio_ext)
            os.link(TRACK_DIR + track, mp_dir + 'presenter.' + audio_ext)

        # Make a zip
        mp_archive = 'mediapackage-' + mp_id
        shutil.make_archive(ZIP_DIR + mp_archive, 'zip', mp_dir)
    except:
        log.error('failed to create mediapackage zip:', exc_info=True)
        return None
    finally:
        # Clean up
        shutil.rmtree(mp_dir, True)

    log.info("created mediapackage zip")
    return mp_archive + '.zip'


def submit_mediapackage(filename):
    # choose a random ingest server if more than one
    ingest_server = random.choice(Opencast['ingests'].split(','))
    log.debug('ingest server ' + ingest_server)

    # Create and ingest the mediapackage POST request to opencast ingest endpoint
    edit = Ingest['edit.freq'] > random.random()
    if edit:
        publish = False
    else:
        publish = Ingest['publish'] == 'True'

    url = '{0}{1}{2}'.format(ingest_server, INGEST_ENDPOINT, Ingest['workflow'])
    headers = {'X-Requested-Auth': 'Digest'}
    files = {'mediapackage': open(ZIP_DIR + filename, 'rb')}
    fields = {'publishOaiPmh': publish,
              'editRecording': edit,
              'emailAddresses': Ingest['email']}
    log.info('workflow parameters, publish: %(publishOaiPmh)s, edit: %(editRecording)s', fields)

    try:
        log.info('starting ingest of mediapackage')
        response = requests.post(url, headers=headers, auth=HTTPDigestAuth(Opencast['account'], Opencast['password']),
                          data=fields, files=files)

        # Check the response status code is 200
        if response.status_code is 200:
            log.info('server successfully ingested mediapackage')
            return True
        else:
            log.error('server failed to ingest mediapackage, returned status code: ' + str(response.status_code))
            return False
    except:
        log.error('failed to upload mediapackage:', exc_info=True)
        return False
    finally:
        # Clean up
        os.remove(ZIP_DIR + filename)


# START

# logging
logging.basicConfig(format='%(asctime)-15s %(levelname)s - (%(module)s:%(lineno)d) %(message)s')
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

# read configuration
config = ConfigParser.ConfigParser()
config.read('simulation.properties')

# config dicts
Opencast = {}
Ingest = {}
Mediapackages = {}

if config.has_section('opencast'):
    Opencast = get_config_section(config, 'opencast')
else:
    log.error('config missing [opencast] section')
    exit(1)

if config.has_section('ingest'):
    Ingest = get_config_section(config, 'ingest')
else:
    log.error('config missing [ingest] section')
    exit(1)

if config.has_section('mediapackages'):
    Mediapackages = get_config_section(config, 'mediapackages')
else:
    log.error('config missing [mediapackages] section')
    exit(1)

# set up template env
Templates = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR)
)

# run the simulation
count = Ingest['count']
num_profiles = Mediapackages['profiles']

for i in range(count):
    select_freq = random.random()
    freq = 0.0
    select_profile = 0
    while freq < select_freq and select_profile < num_profiles:
        select_profile += 1
        freq += Mediapackages['profile.{0}.freq'.format(select_profile)]

    profile = get_profile(select_profile)

    log.info('creating mediapackage {0}/{1} type {2} duration {3}h'.format(i+1, count, profile['type'],
                                                                           profile['duration']))
    mediapackage = create_mediapackage(profile)

    if mediapackage is not None:
        submit_mediapackage(mediapackage)
