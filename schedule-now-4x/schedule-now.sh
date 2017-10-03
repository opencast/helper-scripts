#!/bin/bash

CAPTURE_AGENT="pyca"
HOST="http://localhost:8080"
USER="opencast_system_account"
PASSWORD="CHANGE_ME"

set -eux

if [ "$#" -eq 0 ]; then
    START_MIN=1
    END_MIN=2
elif [ "$#" -eq 2 ]; then
    START_MIN="${1}"
    END_MIN="${2}"
else
    echo "Usage: ${0} [start_min end_min]"
fi

TMP_MP="$(mktemp)"
TMP_DC="$(mktemp)"
START="$(date -d "${START_MIN} min" --utc +%Y-%m-%dT%H:%MZ)"
END="$(date -d "${END_MIN} min" --utc +%Y-%m-%dT%H:%MZ)"

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
  <dcterms:spatial>'${CAPTURE_AGENT}'</dcterms:spatial>
  <dcterms:title>Demo event</dcterms:title>
</dublincore>' > "${TMP_DC}"

# Create media package
curl -f --digest -u ${USER}:${PASSWORD} -H "X-Requested-Auth: Digest" \
  "${HOST}/ingest/createMediaPackage" -o "${TMP_MP}"

# Add DC catalog
curl -f --digest -u ${USER}:${PASSWORD} -H "X-Requested-Auth: Digest" \
  "${HOST}/ingest/addDCCatalog" -F "mediaPackage=<${TMP_MP}" \
  -F "dublinCore=<${TMP_DC}" -o "${TMP_MP}"

curl -v -i --digest -u ${USER}:${PASSWORD} \
    -H "X-Requested-Auth: Digest" \
    "${HOST}/ingest/schedule/fast" \
    -F "mediaPackage=<${TMP_MP}"

rm -f "${TMP_MP}" "${TMP_DC}"
