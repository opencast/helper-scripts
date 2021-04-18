#!/bin/sh

SERVER='https://develop.opencast.org'
LOGIN='admin:opencast'
VIDEO_FILE='video.webm'
WORKFLOW='fast'

set -eux

# Generate title and name
TITLE=$(telnet bofh.jeffballard.us 666 2>&- | \
	sed -e 's/^Your excuse is: //;tx;d;:x')
NAME=$(curl -s 'http://www.richyli.com/randomname/' | \
	sed -e 's/^.*>\([^>(]*\) (Try in .*$/\1/;tx;d;:x')

# Ingest media
curl -f -i -u ${LOGIN} \
	"${SERVER}/ingest/addMediaPackage/${WORKFLOW}" \
	-F flavor="presentation/source" \
	-F "BODY=@${VIDEO_FILE}" -F title="${TITLE}" \
	-F creator="${NAME}"
