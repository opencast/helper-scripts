#!/bin/bash

set -eux

HOST="https://develop.opencast.org"
USER="opencast_system_account"
PASSWORD="CHANGE_ME"
WORKFLOW='fast'

TMP_MP="$(mktemp)"
TMP_DC="$(mktemp)"
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
  <dcterms:title>Demo event</dcterms:title>
</dublincore>' > "${TMP_DC}"

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

# Add Track
curl -f --digest -u ${USER}:${PASSWORD} -H "X-Requested-Auth: Digest" \
  "${HOST}/ingest/addTrack" -F flavor=presentation/source \
  -F "mediaPackage=<${TMP_MP}" -F Body=@video.webm -o "${TMP_MP}"

curl -f -v -i --digest -u ${USER}:${PASSWORD} \
    -H "X-Requested-Auth: Digest" \
    "${HOST}/ingest/ingest/${WORKFLOW}" \
    -F "mediaPackage=<${TMP_MP}"

rm -f "${TMP_MP}" "${TMP_DC}"
