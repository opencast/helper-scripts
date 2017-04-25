#!/bin/bash

NUMBER_OF_INGESTS=3
SERVER='http://localhost:8080'
DIGEST_LOGIN='opencast_system_account:CHANGE_ME'
VIDEO_FILE=/home/eugen/Downloads/video.mp4

if [ ! -f "${VIDEO_FILE}" ]; then
	echo 'File des not exist. Exiting...'
	exit 1
fi

for _ in $(seq 1 ${NUMBER_OF_INGESTS}); do

	# NAME
	NAME="$(python -c 'import random; list = open("names.txt", "r"); names = list.readlines(); names = [x.strip() for x in names]; list.close(); print(random.choice(names));')"

	# TITLE
	TITLE="$(python -c 'import random; list = open("excuses.txt", "r"); excuses = list.readlines(); excuses = [x.strip() for x in excuses]; list.close(); print(random.choice(excuses));')"
	LANGUAGE="$(python -c 'import random; print(random.choice([ "ar", "bg", "ca", "zh", "zt", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "de", "el", "ht", "iw", "hi", "hu", "it", "ja", "ko", "lv", "lt", "ms", "mt", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk", "ur", "vi", "cy"]))')"
	QUERY=$(echo -n "${TITLE}"|python -c "import urllib,sys; print urllib.urlencode({'src':sys.stdin.read(), 'dir':'en/${LANGUAGE}', 'provider':'microsoft', 'ctrl':'target'})")
	NEWTITLE=$(curl -s 'http://translation2.paralink.com/do.asp' --data "${QUERY}" | grep 'top.GEBI(' | cut -d'"' -f2)
	[ -n "$NEWTITLE" ] && TITLE="${NEWTITLE}"

	# DESCRIPTION
	DESCRIPTION="$(python -c 'import random; list = open("excuses.txt", "r"); excuses = list.readlines(); excuses = [x.strip() for x in excuses]; list.close(); print(random.choice(excuses));')"
	LANGUAGE="$(python -c 'import random; print(random.choice([ "ar", "bg", "ca", "zh", "zt", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "de", "el", "ht", "iw", "hi", "hu", "it", "ja", "ko", "lv", "lt", "ms", "mt", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk", "ur", "vi", "cy"]))')"
	QUERY=$(echo -n "${DESCRIPTION}"|python -c "import urllib,sys; print urllib.urlencode({'src':sys.stdin.read(), 'dir':'en/${LANGUAGE}', 'provider':'microsoft', 'ctrl':'target'})")
	NEWDESCRIPTION=$(curl -s 'http://translation2.paralink.com/do.asp' --data "${QUERY}" | grep 'top.GEBI(' | cut -d'"' -f2)
	[ -n "$NEWDESCRIPTION" ] && DESCRIPTION="${NEWDESCRIPTION}"
	
	# LICENSE
	LICENSE="$(python -c 'import random; list = open("excuses.txt", "r"); excuses = list.readlines(); excuses = [x.strip() for x in excuses]; list.close(); print(random.choice(excuses));')"
	LANGUAGE="$(python -c 'import random; print(random.choice([ "ar", "bg", "ca", "zh", "zt", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "de", "el", "ht", "iw", "hi", "hu", "it", "ja", "ko", "lv", "lt", "ms", "mt", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk", "ur", "vi", "cy"]))')"
	QUERY=$(echo -n "${LICENSE}"|python -c "import urllib,sys; print urllib.urlencode({'src':sys.stdin.read(), 'dir':'en/${LANGUAGE}', 'provider':'microsoft', 'ctrl':'target'})")
	NEWLICENSE=$(curl -s 'http://translation2.paralink.com/do.asp' --data "${QUERY}" | grep 'top.GEBI(' | cut -d'"' -f2)
	[ -n "$NEWLICENSE" ] && LICENSE="${NEWLICENSE}"

	# SOURCE
	SOURCE="$(python -c 'import random; list = open("excuses.txt", "r"); excuses = list.readlines(); excuses = [x.strip() for x in excuses]; list.close(); print(random.choice(excuses));')"
	LANGUAGE="$(python -c 'import random; print(random.choice([ "ar", "bg", "ca", "zh", "zt", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "de", "el", "ht", "iw", "hi", "hu", "it", "ja", "ko", "lv", "lt", "ms", "mt", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk", "ur", "vi", "cy"]))')"
	QUERY=$(echo -n "${SOURCE}"|python -c "import urllib,sys; print urllib.urlencode({'src':sys.stdin.read(), 'dir':'en/${LANGUAGE}', 'provider':'microsoft', 'ctrl':'target'})")
	NEWSOURCE=$(curl -s 'http://translation2.paralink.com/do.asp' --data "${QUERY}" | grep 'top.GEBI(' | cut -d'"' -f2)
	[ -n "$NEWSOURCE" ] && SOURCE="${NEWSOURCE}"

	# SUBJECT
	SUBJECT="$(python -c 'import random; list = open("excuses.txt", "r"); excuses = list.readlines(); excuses = [x.strip() for x in excuses]; list.close(); print(random.choice(excuses));')"
	LANGUAGE="$(python -c 'import random; print(random.choice([ "ar", "bg", "ca", "zh", "zt", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "de", "el", "ht", "iw", "hi", "hu", "it", "ja", "ko", "lv", "lt", "ms", "mt", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk", "ur", "vi", "cy"]))')"
	QUERY=$(echo -n "${SUBJECT}"|python -c "import urllib,sys; print urllib.urlencode({'src':sys.stdin.read(), 'dir':'en/${LANGUAGE}', 'provider':'microsoft', 'ctrl':'target'})")
	NEWSUBJECT=$(curl -s 'http://translation2.paralink.com/do.asp' --data "${QUERY}" | grep 'top.GEBI(' | cut -d'"' -f2)
	[ -n "$NEWSUBJECT" ] && SUBJECT="${NEWSUBJECT}"

	# CONTRIBUTOR
	CONTRIBUTOR="$(python -c 'import random; list = open("excuses.txt", "r"); excuses = list.readlines(); excuses = [x.strip() for x in excuses]; list.close(); print(random.choice(excuses));')"
	LANGUAGE="$(python -c 'import random; print(random.choice([ "ar", "bg", "ca", "zh", "zt", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "de", "el", "ht", "iw", "hi", "hu", "it", "ja", "ko", "lv", "lt", "ms", "mt", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk", "ur", "vi", "cy"]))')"
	QUERY=$(echo -n "${CONTRIBUTOR}"|python -c "import urllib,sys; print urllib.urlencode({'src':sys.stdin.read(), 'dir':'en/${LANGUAGE}', 'provider':'microsoft', 'ctrl':'target'})")
	NEWCONTRIBUTOR=$(curl -s 'http://translation2.paralink.com/do.asp' --data "${QUERY}" | grep 'top.GEBI(' | cut -d'"' -f2)
	[ -n "$NEWCONTRIBUTOR" ] && CONTRIBUTOR="${NEWCONTRIBUTOR}"

	# RIGHTSHOLDER
	RIGHTSHOLDER="$(python -c 'import random; list = open("excuses.txt", "r"); excuses = list.readlines(); excuses = [x.strip() for x in excuses]; list.close(); print(random.choice(excuses));')"
	LANGUAGE="$(python -c 'import random; print(random.choice([ "ar", "bg", "ca", "zh", "zt", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "de", "el", "ht", "iw", "hi", "hu", "it", "ja", "ko", "lv", "lt", "ms", "mt", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk", "ur", "vi", "cy"]))')"
	QUERY=$(echo -n "${RIGHTSHOLDER}"|python -c "import urllib,sys; print urllib.urlencode({'src':sys.stdin.read(), 'dir':'en/${LANGUAGE}', 'provider':'microsoft', 'ctrl':'target'})")
	NEWRIGHTSHOLDER=$(curl -s 'http://translation2.paralink.com/do.asp' --data "${QUERY}" | grep 'top.GEBI(' | cut -d'"' -f2)
	[ -n "$NEWRIGHTSHOLDER" ] && RIGHTSHOLDER="${NEWRIGHTSHOLDER}"
	
	# SOME INFORMATION
	#echo "NAME: ${NAME}"
	#echo "TITLE: ${TITLE}"
	#echo "DESCRIPTION: ${DESCRIPTION}"
	#echo "LICENSE: ${LICENSE}"
	#echo "SOURCE: ${SOURCE}"
	#echo "SUBJECT: ${SUBJECT}"
	#echo "CONTRIBUTOR: ${CONTRIBUTOR}"
	#echo "RIGHTSHOLDER: ${RIGHTSHOLDER}"

	# Ingest media
	curl -f -i --digest -u ${DIGEST_LOGIN} \
		-H "X-Requested-Auth: Digest" \
		"${SERVER}/ingest/addMediaPackage/fast" \
	  	-F flavor="presenter/source" \
	  	-F "BODY=@${VIDEO_FILE}" -F title="${TITLE}" \
	  	-F creator="${NAME}" \
	  	-F description="${DESCRIPTION}" \
	  	-F language="${LANGUAGE}" \
	  	-F license="${LICENSE}" \
	  	-F source="${SOURCE}" \
	  	-F subject="${SUBJECT}" \
	  	-F contributor="${CONTRIBUTOR}" \
	  	-F rightsHolder="${RIGHTSHOLDER}"

done
