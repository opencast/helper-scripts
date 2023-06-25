#!/usr/bin/env python3
import os
import re
import requests
from requests.auth import HTTPBasicAuth
import yaml
import xml.etree.cElementTree
from xml.etree import ElementTree

config = {}

# Set status output message & style
def print_status(ok, title, err=None):
    color = '\033[92m' if ok else '\033[91m'
    text = ' ok ' if ok else 'fail'
    print(f'  [{color}{text}\033[0m]: {title}')
    if err:
        print(f'    → {err}')

# Send POST request and get status
def post(title, path, **kwargs):
    auth = HTTPBasicAuth(
            config['server']['destination-username'],
            config['server']['destination-password'])
    server = config['server']['destination-url']
    try:
        r = requests.post(f'{server}{path}', auth=auth, **kwargs)
        r.raise_for_status()
        print_status(r.ok, title)
    except Exception as e:
        print_status(False, title, str(e).strip())

# Send GET request and get status
def get(title, path, params):
    auth = HTTPBasicAuth(
            config['server']['source-username'],
            config['server']['source-password'])
    server = config['server']['source-url']
    try:
        r = requests.get(url=f'{server}{path}', auth=auth, params=params)
        r.raise_for_status()
        print_status(r.ok, title)
        return r.content

    except Exception as e:
        print_status(False, title, str(e).strip())

# Load YAML configuration file as global variable
def load_config():
    global config
    with open('media.yml', 'r') as f:
        config = yaml.safe_load(f)
# Convert string to xml object
def stringToXml(payload):
    return ElementTree.fromstring(payload)

# Write xml tree to a .xml file
def writeTreeToFile(xml, pathToFile):
    dir = config['exportData']['exportDir']
    if not os.path.exists(dir):
        os.mkdir(dir)
    with open(dir + pathToFile, 'w') as f:
        xml.write(f, encoding='unicode')

# Remove all namespaces from a xml tree
def strip_namespaces(el):
  if el.tag.startswith("{"):
    el.tag = el.tag.split('}', 1)[1]
  for k in el.attrib.keys():
    if k.startswith("{"):
      k2 = k.split('}', 1)[1]
      el.attrib[k2] = el.attrib[k]
      del el.attrib[k]
  for child in el:
    strip_namespaces(child)


# Clean the export directory
def clean_dir():
    dir = config['exportData']['exportDir']
    if not os.path.exists(dir):
        os.mkdir(dir)
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

# Get event/series limits as string for logging
def get_limits_string(limit, offset, total):
    startWithZero = config['exportData']['startWithZero']
    first = offset + int(not startWithZero)
    if offset + limit <= total:
        last = offset + limit - int(startWithZero)
    else:
        last = total - int(startWithZero)

    numbers = str(first)
    if first != last:
        numbers = numbers + '-' + str(last)

    return numbers

# Count existing series from source opencast
def get_series_count():
    params = {'episodes':'false', 'limit':'1', 'offset':'0'}
    endpoint = '/search/series.xml'
    title = 'Getting total number of series'
    xml = stringToXml(get(title, endpoint, params))
    return (int(xml.attrib['total']))

# Count existing events from source opencast
def get_events_count():
    params = {'limit':'1', 'offset':'0'}
    endpoint = '/search/episode.xml'
    title = 'Getting total number of events'
    xml = stringToXml(get(title, endpoint, params))

    return (int(xml.attrib['total']))

# Get series from search endpoint as xml tree objects
def get_series_xml_tree(sort, limit , offset, limitsString):

    params = {'episodes':'false', 'sort':sort, 'limit':limit, 'offset':offset, 'sign':True}
    endpoint = '/search/series.xml'
    title = 'Getting series [' + limitsString + ']'

    xmlSeries = stringToXml(get(title, endpoint, params))

    exportedTree = ElementTree.ElementTree(xmlSeries)
    exportedRoot = exportedTree.getroot()

    seriesTree = ElementTree.ElementTree()
    seriesRoot = ElementTree.Element('exportedSeries')
    seriesTree._setroot(seriesRoot)
    nsSeries = config['exportData']['nsSeries']

    for result in exportedRoot.iter(nsSeries):
        singleSeriesRoot = ElementTree.Element('series')

        seriesId = result.attrib['id']
        params = {}
        endpoint = '/series/' + seriesId + '.xml'
        title = 'Exporting series id "' + seriesId + '"'

        strip_namespaces(result)
        aclTree = extract_acl(result)
        dcTree = ElementTree.ElementTree(stringToXml(get(title, endpoint, params)))

        singleSeriesRoot.append(aclTree.getroot())
        singleSeriesRoot.append(dcTree.getroot())
        seriesRoot.append(singleSeriesRoot)
        singleSeriesRoot.attrib['id'] = seriesId
    return seriesTree

# Get events from search endpoint as xml tree objects
def get_events_xml_tree(sort, limit , offset, limitsString):

    params = {'sort':sort, 'limit':limit, 'offset':offset, 'sign':True}
    endpoint = '/search/episode.xml'
    title = 'Getting event(s) [' + limitsString + ']'

    xmlEvents = stringToXml(get(title, endpoint, params))

    exportedTree = ElementTree.ElementTree(xmlEvents)
    exportedRoot = exportedTree.getroot()

    eventTree = ElementTree.ElementTree()
    eventRoot = ElementTree.Element("exportedEvents")
    eventTree._setroot(eventRoot)
    nsMediapackage = config['exportData']['nsMediapackage']

    for result in exportedRoot.iter(nsMediapackage):
        eventRoot.append(result)

    return eventTree

# Extract acl tree from single series tree
def extract_acl(singleSeriesTree):
    aclTree = ElementTree.ElementTree()
    aclRoot = ElementTree.Element('acl', xmlns="http://org.opencastproject.security")
    aclTree._setroot(aclRoot)
    for ace in singleSeriesTree.iter('ace'):
         aclRoot.append(ace)
    return aclTree

# Export all series from source opencast
def export_series():
    sort = config['exportData']['sortSeriesBy']
    limit = config['exportData']['limit']
    seriesFilePrefix = config['exportData']['seriesFilePrefix']
    nsSeries = config['exportData']['nsMediapackage']

    offset = 0
    totalSeries = get_series_count()

    print('Trying to export ' + str(totalSeries) + ' series from source opencast')

    while offset < totalSeries:
        limitsString = get_limits_string(limit, offset, totalSeries)
        xmlTreeSeries = get_series_xml_tree(sort, limit, offset, limitsString)
        xmlFilePath = seriesFilePrefix + limitsString + '.xml'

        offset = offset + limit
        writeTreeToFile(xmlTreeSeries,xmlFilePath)

# Export all series from source opencast
def export_mediapackages():
    sort = config['exportData']['sortEventsBy']
    limit = config['exportData']['limit']
    eventFilePrefix = config['exportData']['eventFilePrefix']

    offset = 0
    totalEvents = get_events_count()

    print('Trying to export ' + str(totalEvents) + ' events from source opencast')

    while offset < totalEvents:
        limitsString = get_limits_string(limit, offset, totalEvents)
        xmlTreeEvents = get_events_xml_tree(sort, limit, offset, limitsString)
        xmlFilePath = eventFilePrefix + limitsString + '.xml'

        offset = offset + limit
        writeTreeToFile(xmlTreeEvents,xmlFilePath)

# import all series in destination opencast
def import_series():
    dir = config['exportData']['exportDir']
    filePrefix = config['exportData']['seriesFilePrefix']

    print('Trying to import series in destination opencast')
    # REPEAT for all Files
    for filename in os.listdir(dir):

        # Load MULTIPLE SERIES tree from File
        if re.match(filePrefix + '.+xml', filename):
            with open(os.path.join(dir, filename), 'r') as f:
                xmlData = stringToXml(f.read().rstrip())

            # Extract SINGLE SERIES tree from MULTIPLE SERIES tree
            nsSeries = 'series'
            seriesTree = ElementTree.ElementTree(xmlData)
            seriesRoot = seriesTree.getroot()

            # REPEAT for all SINGLE SERIES trees
            for series in seriesRoot.iter(nsSeries):

                # Extract ACL TREE from SERIES tree
                aclTree = ElementTree.ElementTree()
                aclTree._setroot(series[0])

                # Extract DC TREE from SERIES tree
                nsDc = config['exportData']['nsSeriesDc']
                dcTree = ElementTree.ElementTree()
                dcTree._setroot(series[1])

                # Send ACL & DC tree to opencast to create SERIES
                data = {
                    'acl':ElementTree.tostring(aclTree.getroot(), encoding='unicode', method='xml'),
                    'series':ElementTree.tostring(dcTree.getroot(), encoding='unicode', method='xml')
                }
                endpoint = '/series/'
                title = 'Importing series id "' + series.attrib['id'] + '"'
                post(title, endpoint, data=data)

# import all events in destination opencast
def import_mediapackages():
    dir = config['exportData']['exportDir']
    filePrefix = config['exportData']['eventFilePrefix']

    print('Trying to import events in destination opencast')

    # REPEAT for all Files
    for filename in os.listdir(dir):

        # Load MULTIPLE EVENTS tree from File
        if re.match(filePrefix + '.+xml', filename):
            with open(os.path.join(dir, filename), 'r') as f:
                xmlData = stringToXml(f.read().rstrip())

            # Extract SINGLE EVENT tree from MULTIPLE EVENTS tree
            nsEvents = config['exportData']['nsMediapackage']
            eventsTree = ElementTree.ElementTree(xmlData)
            eventsRoot = eventsTree.getroot()

            # REPEAT for all SINGLE EVENT trees
            for event in eventsRoot.iter(nsEvents):
                singleEventTree = ElementTree.ElementTree()
                singleEventTree._setroot(event)
                mediapackageString = singleEventTree.getroot().text

                # Send SINGLE EVENT tree to opencast to create SERIES
                ingestWorkflow = config['exportData']['ingestWorkflow']
                data = {
                    'mediaPackage': mediapackageString,
                    'workflowDefinitionId': ingestWorkflow,
                    'workflowInstanceId': ''
                }

                endpoint = '/ingest/ingest'
                mediapackageXml = stringToXml(mediapackageString)
                title = 'Importing event id "' + mediapackageXml.attrib['id'] + '"'
                post(title, endpoint, data=data)

# Main Loop
if __name__ == '__main__':
    load_config()
    clean_dir()
    export_series()
    export_mediapackages()
    import_series()
    import_mediapackages()
    #clean_dir()