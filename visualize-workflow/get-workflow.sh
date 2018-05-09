#!/bin/sh
set -ue

LOGIN=opencast_system_account:CHANGE_ME
HOST=https://develop.opencast.org
ID=$1

curl -f --digest -u "${LOGIN}" -H "X-Requested-Auth: Digest" \
  -o workflow.json "${HOST}/workflow/instance/${ID}.json"
