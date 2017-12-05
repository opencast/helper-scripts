#/bin/python

import json

import json
from pprint import pprint

csvString='Titel;Startdatum;SERIES;ID\n'

with open('events.json') as data_file:
    data = json.load(data_file)
for u in data['results']:
    Seriestitle = ''
    if u.get('series'):
        Seriestitle = u.get('series')['title']

    csvString+=u['title'] + ';' + u['technical_start'] + ';' + Seriestitle + ';' + u['id'] + '\n'

print csvString

file = open('events.csv','w')
file.write(csvString.encode('utf-8'))
file.close()
