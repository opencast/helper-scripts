#!/bin/bash

NUMBER_OF_INGESTS=1
SERVER='http://localhost:8080'
DIGEST_LOGIN='opencast_system_account:CHANGE_ME'
VIDEO_FILE=/home/eugen/Downloads/video.mp4

if [ ! -f "${VIDEO_FILE}" ]; then
	echo 'File des not exist. Exiting...'
	exit 1
fi

for _ in $(seq 1 ${NUMBER_OF_INGESTS}); do

	# Generate title and name
	TITLE=$(telnet bofh.jeffballard.us 666 2>&- | \
		sed -e 's/^Your excuse is: //;tx;d;:x')
	NAME=$(curl -s 'http://www.richyli.com/randomname/' | \
		sed -e 's/^.*>\([^>(]*\) (Try in .*$/\1/;tx;d;:x')

	# Translate title
	LANGUAGE="$(python -c 'import random; print(random.choice([ "ar", "bg",
		"ca", "zh", "zt", "hr", "cs", "da", "nl", "en", "et", "fi", "fr",
		"de", "el", "ht", "iw", "hi", "hu", "it", "ja", "ko",
		"lv", "lt", "ms", "mt", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk",
		"sl", "es", "sw", "sv", "th", "tr", "uk", "ur", "vi", "cy"]))')"
	QUERY=$(echo -n "${TITLE}"|python -c "import urllib,sys; print urllib.urlencode({'src':sys.stdin.read(), 'dir':'en/${LANGUAGE}', 'provider':'microsoft', 'ctrl':'target'})")
	NEWTITLE=$(curl -s 'http://translation2.paralink.com/do.asp' --data "${QUERY}" | grep 'top.GEBI(' | cut -d'"' -f2)
	[ -n "$NEWTITLE" ] && TITLE="${NEWTITLE}"

	echo "### NUMBER_OF_INGESTS:"
	echo "${NUMBER_OF_INGESTS}"
	echo "### SERVER:"
	echo "${SERVER}"
	echo "### DIGEST_LOGIN:"
	echo "${DIGEST_LOGIN}"
	echo "### VIDEO_FILE:"
	echo "${VIDEO_FILE}"
	echo "### TITLE:"
	echo "${TITLE}"
	echo "### NAME:"
	echo "${NAME}"
	echo "### LANGUAGE:"
	echo "${LANGUAGE}"
	echo "### QUERY:"
	echo "${QUERY}"
	echo "### NEWTITLE:"
	echo "${NEWTITLE}"

	# Ingest media
	curl -f -i --digest -u ${DIGEST_LOGIN} \
		-H "X-Requested-Auth: Digest" \
		"${SERVER}/ingest/addMediaPackage/fast" \
		-F flavor="presenter/source" \
		-F "BODY=@${VIDEO_FILE}" -F title="${TITLE}" \
		-F creator="${NAME}" \
		-F description="TEST TEST TEST --- description" \
		-F language="TEST TEST TEST --- ${LANGUAGE}" \
		-F license="TEST TEST TEST --- license" \
		-F rights="TEST TEST TEST --- rights" \
		-F source="TEST TEST TEST --- source" \
		-F subject="TEST TEST TEST --- subject" \
		-F contributor="TEST TEST TEST --- contributor" \
		-F rightsHolder="TEST TEST TEST --- rightsHolder" \
		-F replaces="TEST TEST TEST --- replaces" 

done

	#abstract: Episode metadata value
	#accessRights: Episode metadata value
	#available: Episode metadata value
	#contributor: Episode metadata value
	#coverage: Episode metadata value
	#created: Episode metadata value
	#creator: Episode metadata value
	#date: Episode metadata value
	#description: Episode metadata value
	#extent: Episode metadata value
	#format: Episode metadata value
	#identifier: Episode metadata value
	#isPartOf: Episode metadata value
	#isReferencedBy: Episode metadata value
	#isReplacedBy: Episode metadata value
	#language: Episode metadata value
	#license: Episode metadata value
	#publisher: Episode metadata value
	#relation: Episode metadata value
	#replaces: Episode metadata value
	#rights: Episode metadata value
	#rightsHolder: Episode metadata value
	#source: Episode metadata value
	#spatial: Episode metadata value
	#subject: Episode metadata value
	#temporal: Episode metadata value
	#title: Episode metadata value
	#type: Episode metadata value
	#episodeDCCatalogUri: URL of episode DublinCore Catalog
	#episodeDCCatalog: Episode DublinCore Catalog
	#seriesDCCatalogUri: URL of series DublinCore Catalog
	#seriesDCCatalog: Series DublinCore Catalog
	#mediaUri: URL of a media track file
