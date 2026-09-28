#!/bin/bash

set -ue

FROM_HOST="https://develop.opencast.org"
FROM_CREDS="opencast_system_account:CHANGE_ME"
TO_HOST="http://localhost"
TO_CREDS="opencast_system_account:CHANGE_ME"

search=""
if [ $# -eq 1 ]; then
  search="filter=identifier:$1"
fi

curl -s -f --digest -u "$FROM_CREDS" -H 'X-Requested-Auth: Digest' $FROM_HOST/api/series?$search | jq -r '.[].identifier' | while read identifier
do
  #This spits out *just* the primary DC metadata in a semi-useful format, but not the extended metadata!
  #echo "Series"
  #ocreq http://localhost/api/series/$identifier | jq > $identifier.json

  echo "Fetching ACL for $identifier from $FROM_HOST"
  curl -s -f --digest -u "$FROM_CREDS" -H 'X-Requested-Auth: Digest' $FROM_HOST/api/series/$identifier/acl | jq > $identifier-acl.json
  #If the series ACL is completely blank, fill in an empty one
  if [ "$(cat $identifier-acl.json)" == "" ]; then
    echo "[]" > $identifier-acl.json
  fi

  echo "Fetching full set of series metadata for $identifier from $FROM_HOST"
  curl -s -f --digest -u "$FROM_CREDS" -H 'X-Requested-Auth: Digest' $FROM_HOST/api/series/$identifier/metadata | jq > $identifier-metadata.json
  if [ "$(cat $identifier-metadata.json)" == "" ]; then
    echo "Skipping $identifier, metadata is blank!"
    continue
  fi
#done

#ls *-metadata.json | sed 's/-metadata.json//g' | while read identifier
#do


  if [ $(curl -s -o /dev/null -w "%{http_code}\n" -f --digest -u "$TO_CREDS" -H 'X-Requested-Auth: Digest' $TO_HOST/api/series/$identifier) != "404" ]; then
    echo "Skipping $identifier, series may already exist!"
    continue
  fi

  CATALOGS=$(cat $identifier-metadata.json | jq 'map({title, flavor, fields: .fields | map(select(.id != "createdBy")) | map({id, value})})')
  #echo "$CATALOGS"

  echo "Creating series on $TO_HOST"
  curl -f --digest -u "$TO_CREDS" -H 'X-Requested-Auth: Digest' -X POST $TO_HOST/api/series \
    -d "metadata=$CATALOGS" \
    -d "acl=$(cat $identifier-acl.json)"

  rm -f $identifier*.json
done
