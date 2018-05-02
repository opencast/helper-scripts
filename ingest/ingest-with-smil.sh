#!/bin/bash

#set -eux

randomString() {
  od -vN 16 -An -tx1 /dev/urandom | tr -d " \\n"; echo
}

HOST="http://localhost:8080"
USER="opencast_system_account"
PASSWORD="CHANGE_ME"
WORKFLOW='ng-schedule-and-upload'

TMP_MP="$(mktemp)"
TMP_DC="$(mktemp)"
TMP_SMIL="$(mktemp /tmp/smilXXXX --suffix=.xml)"
START="$(date -d "1 min" --utc +%Y-%m-%dT%H:%MZ)"
END="$(date -d "2 min" --utc +%Y-%m-%dT%H:%MZ)"

echo '<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<dublincore xmlns="http://www.opencastproject.org/xsd/1.0/dublincore/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dcterms:creator>demo</dcterms:creator>
  <dcterms:contributor>demo</dcterms:contributor>
  <dcterms:created xsi:type="dcterms:W3CDTF">'"${START}"'</dcterms:created>
  <dcterms:temporal xsi:type="dcterms:Period">start='"${START}"'; end='"${END}"'; scheme=W3C-DTF;</dcterms:temporal>
  <dcterms:description>demo</dcterms:description>
  <dcterms:subject>demo</dcterms:subject>
  <dcterms:language>demo</dcterms:language>
  <dcterms:spatial>pyca</dcterms:spatial>
  <dcterms:title>Edited demo event</dcterms:title>
</dublincore>' > "${TMP_DC}"

# SMIL Variables
TRACK_PG1="$(randomString)"
MP_ID=""
TRACK_ID=""
TRACK_URL=""

# Suppose the video.mp4 track has length 60000ms and is edited to include only two segments where
# segment 1: 10000ms - 20000ms
# segment 2: 30000ms - 40000ms
#
# i.e. segments with timestamps 0ms - 10000ms, 20000ms - 30000ms, 40000ms - 60000ms are removed/cut

echo '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<smil version="3.0" baseProfile="Language" xmlns="http://www.w3.org/ns/SMIL"
    xml:id="s-'"$( randomString )"'" xmlns:oc="http://smil.opencastproject.org">
  <head xmlns="http://www.w3.org/1999/xhtml" xml:id="h-'"$( randomString )"'">
    <meta name="media-package-id" content="%MP_ID%" xml:id="meta-'"$( randomString )"'"/>
    <meta name="track-duration" content="60000ms" xml:id="meta-'"$( randomString )"'"/>
    <paramGroup xml:id="pg-'"${TRACK_PG1}"'">
      <param valuetype="data" name="track-id" value="%TRACK_ID%" xml:id="param-'"$( randomString )"'"/>
      <param valuetype="data" name="track-src" value="%TRACK_URL%" xml:id="param-'"$( randomString )"'"/>
      <param valuetype="data" name="track-flavor" value="presenter/source" xml:id="param-'"$( randomString )"'"/>
    </paramGroup>
  </head>
  <body xmlns="http://www.w3.org/1999/xhtml" xml:id="b-'"$( randomString )"'">
    <par xml:id="par-'"$( randomString )"'">
      <video clipBegin="10000ms" clipEnd="20000ms" src="%TRACK_URL%" paramGroup="pg-'"${TRACK_PG1}"'" xml:id="param-'"$( randomString )"'"/>
    </par>
    <par xml:id="par-'"$( randomString )"'">
      <video clipBegin="30000ms" clipEnd="40000ms" src="%TRACK_URL%" paramGroup="pg-'"${TRACK_PG1}"'" xml:id="param-'"$( randomString )"'"/>
    </par>
  </body>
</smil>' > "${TMP_SMIL}"

# Note that %MP_ID%, %TRACK_ID% and %TRACK_URL in the XML above depend on responses by the server and cannot be randomised.

# END SMIL Variables

# Create media package
curl -f --digest -u ${USER}:${PASSWORD} -H "X-Requested-Auth: Digest" \
  "${HOST}/ingest/createMediaPackage" -o "${TMP_MP}"


# Add DC catalog
curl -f --digest -u ${USER}:${PASSWORD} -H "X-Requested-Auth: Digest" \
  "${HOST}/ingest/addDCCatalog" -F "mediaPackage=<${TMP_MP}" \
  -F "dublinCore=<${TMP_DC}" -o "${TMP_MP}"

# Add Track
curl -f --digest -u ${USER}:${PASSWORD} -H "X-Requested-Auth: Digest" \
  "${HOST}/ingest/addTrack" -F flavor=presenter/source \
  -F "mediaPackage=<${TMP_MP}" -F Body=@video.webm -o "${TMP_MP}"

# Prepare SMIL
MP_ID="$(awk -F 'mediapackage id="' '{ print $2 }' "${TMP_MP}" | awk -F '"' '{ print $1}')"
TRACK_ID="$(awk -F 'track id="' '{ print $2 }' "${TMP_MP}" | awk -F '"' '{print $1}')"
TRACK_URL="$(awk -F 'track id="' '{ print $2 }' "${TMP_MP}" | awk -F '</url>' '{print $1}' | awk -F '<url>' '{ print $2 }')"
TRACK_URL=${TRACK_URL//\//\\\/}

sed -i "s/%MP_ID%/$MP_ID/g" "${TMP_SMIL}"
sed -i "s/%TRACK_ID%/$TRACK_ID/g" "${TMP_SMIL}"
sed -i "s/%TRACK_URL%/$TRACK_URL/g" "${TMP_SMIL}"

# Add SMIL
curl -f --digest -u ${USER}:${PASSWORD} -H "X-Requested-Auth: Digest" \
  "${HOST}/ingest/addCatalog" -F flavor=smil/cutting \
  -F "mediaPackage=<${TMP_MP}" -F "Body=@${TMP_SMIL}" -o "${TMP_MP}"

# Start workflow with editor step
curl -f -i --digest -u ${USER}:${PASSWORD} \
    -H "X-Requested-Auth: Digest" \
    "${HOST}/ingest/ingest/${WORKFLOW}" \
    -F "mediaPackage=<${TMP_MP}"

rm -f "${TMP_MP}" "${TMP_DC}" "${TMP_SMIL}"
