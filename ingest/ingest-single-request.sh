#!/bin/sh

NUMBER_OF_INGESTS=2
SERVER='https://develop.opencast.org'
DIGEST_LOGIN='opencast_system_account:CHANGE_ME'
VIDEO_FILE='video.webm'
WORKFLOW='fast'

set -eux

if [ ! -f "${VIDEO_FILE}" ]; then
	echo 'Video file to inbgest: '
	read -r VIDEO_FILE
	if [ ! -f "${VIDEO_FILE}" ]; then
		echo 'File des not exist. Exiting...'
		exit 1
	fi
fi

for _ in $(seq 1 ${NUMBER_OF_INGESTS}); do

	# Generate title and name
	TITLE=$(telnet bofh.jeffballard.us 666 2>&- | \
		sed -e 's/^Your excuse is: //;tx;d;:x')
	NAME=$(curl -s 'http://www.richyli.com/randomname/' | \
		sed -e 's/^.*>\([^>(]*\) (Try in .*$/\1/;tx;d;:x')

	# Ingest media
	curl -f -i --digest -u ${DIGEST_LOGIN} \
		-H "X-Requested-Auth: Digest" \
		"${SERVER}/ingest/addMediaPackage/${WORKFLOW}" \
		-F flavor="presentation/source" \
		-F "BODY=@${VIDEO_FILE}" -F title="${TITLE}" \
		-F creator="${NAME}"

done
