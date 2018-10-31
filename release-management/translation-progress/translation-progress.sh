#!/bin/sh

set -ue

key="$(awk '{print $2};' < ~/.crowdin.yaml)"
curl -s "https://api.crowdin.com/api/project/opencast-community/status?key=$key" \
	| grep 'name\|translated_progress' \
	| tr '\n' ' ' \
	| sed "s/<\\/translated_progress>/\\n/g" \
	| sed 's#^.*<name>\(.*\)</name.*progress>\(.*\)#\2 \1#' \
	| sort -hr \
	| sed 's/^\(.[^ ]\) / \1 /' \
	| sed 's/^\([^ ]\) /  \1 /' \
	| sed '$d'
