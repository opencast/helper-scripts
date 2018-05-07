#!/usr/bin/env python

import json

if __name__ == '__main__':

    csvString = 'titel;start date;series;id\n'

    with open('events.json') as data_file:
        data = json.load(data_file)

    for u in data['results']:
        seriestitle = ''
        if u.get('series'):
            seriestitle = u.get('series')['title']

        csvString += ';'.join((u['title'],
                               u['technical_start'],
                               seriestitle,
                               u['id']))
        csvString += '\n'

    print(csvString)

    with open('events.csv', 'w') as file:
        file.write(csvString.encode('utf-8'))
