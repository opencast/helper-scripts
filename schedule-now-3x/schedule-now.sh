#!/bin/bash

CAPTURE_AGENT="pyca"
SERVER="http://localhost:8080"
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

TMP="$(mktemp)"
NOW="$(date --utc +%Y-%m-%dT%H:%MZ)"
START="$(date -d "${START_MIN} min" --utc +%Y-%m-%dT%H:%MZ)"
END_CALC=$((START_MIN + END_MIN)) #We want the end time to be start time + duration
END="$(date -d "${END_CALC} min" --utc +%Y-%m-%dT%H:%MZ)"

echo '<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<dublincore xmlns="http://www.opencastproject.org/xsd/1.0/dublincore/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dcterms:creator>demo</dcterms:creator>
  <dcterms:contributor>demo</dcterms:contributor>
  <dcterms:created xsi:type="dcterms:W3CDTF">'"${NOW}"'</dcterms:created>
  <dcterms:temporal xsi:type="dcterms:Period">start='"${START}"'; end='"${END}"'; scheme=W3C-DTF;</dcterms:temporal>
  <dcterms:description>demo</dcterms:description>
  <dcterms:subject>demo</dcterms:subject>
  <dcterms:language>demo</dcterms:language>
  <dcterms:spatial>'"${CAPTURE_AGENT}"'</dcterms:spatial>
  <dcterms:title>Demo event</dcterms:title>
</dublincore>' > "${TMP}"

PROPERTIES="event.location=${CAPTURE_AGENT}
org.opencastproject.workflow.definition=fast
"

cat "${TMP}"

curl -i --digest -u "${USER}:${PASSWORD}" \
    -H "X-Requested-Auth: Digest" \
    "${SERVER}/recordings/" \
    -F "dublincore=@${TMP}" \
    -F "agentparameters=${PROPERTIES}"

rm "${TMP}"
