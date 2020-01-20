#!/bin/bash

#set -eux

randomString() {
  od -vN 16 -An -tx1 /dev/urandom | tr -d " \\n"; echo
}

HOST="http://localhost:8080"
USER="admin"
PASSWORD="opencast"
WORKFLOW="direct-publication"

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
  <dcterms:title>Multi-Language Captions</dcterms:title>
</dublincore>' > "${TMP_DC}"


# Create media package
curl -f -u "${USER}:${PASSWORD}" "${HOST}/ingest/createMediaPackage" -o "${TMP_MP}"


# Add DC catalog
curl -f -u "${USER}:${PASSWORD}" \
  "${HOST}/ingest/addDCCatalog" -F "mediaPackage=<${TMP_MP}" \
  -F "dublinCore=<${TMP_DC}" -o "${TMP_MP}"

# Add Track
curl -f -u ${USER}:${PASSWORD} \
  "${HOST}/ingest/addTrack" -F flavor=presenter/source \
  -F "mediaPackage=<${TMP_MP}" -F Body=@webvtt-example.mp4 -o "${TMP_MP}"

# Add Subtitle
curl -f -u "${USER}:${PASSWORD}" \
  "${HOST}/ingest/addAttachment" -F flavor=captions/vtt+en \
  -F "mediaPackage=<${TMP_MP}" -F "Body=@sample-en.vtt" -o "${TMP_MP}"

# Add Subtitle
curl -f -u "${USER}:${PASSWORD}" \
  "${HOST}/ingest/addAttachment" -F flavor=captions/vtt+de \
  -F "mediaPackage=<${TMP_MP}" -F "Body=@sample-de.vtt" -o "${TMP_MP}"

# Start workflow with editor step
curl -f -i -u "${USER}:${PASSWORD}" \
    "${HOST}/ingest/ingest/${WORKFLOW}" \
    -F "mediaPackage=<${TMP_MP}"

rm -f "${TMP_MP}" "${TMP_DC}"
