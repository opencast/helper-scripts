#!/bin/sh

DIGEST_LOGIN='opencast_system_account:CHANGE_ME'
PERIOD='2018-04-01T00:00:00.000Z/2018-11-11T00:00:00.000Z'
FILENAME='events.json'
OPENCASTADMINNODE=https://stable.opencast.org

set -eu

filter="technical_start:${PERIOD}"
curl -f --digest -o "${FILENAME}" -u "${DIGEST_LOGIN}" \
  -H "X-Requested-Auth: Digest" \
  "${OPENCASTADMINNODE}/admin-ng/event/events.json?filter=${filter}"
