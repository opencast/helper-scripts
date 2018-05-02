#!/bin/bash

# set the range of series to be created
# value: <start> <end>
# start value must be greater then end value
SERIES_SEQ="1 1000"

# set #processes should can run asynchronous
# ideal value is a multiple of CPU cores on your system
PARALlEL_PS=64

# opencast URL
OC_URL="http://localhost:8080"
#OC_URL="https://octestallinone.virtuos.uos.de"

# opencast digest user name
OC_DIGEST_USER="opencast_system_account"

# opencast digest user password
OC_DIGEST_PASSWORD="CHANGE_ME"

# opencast series ACL to be used for new series
SERIES_ACL='<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<acl xmlns="http://org.opencastproject.security">
<ace>
<action>read</action>
<allow>true</allow>
<role>ROLE_USER_ADMIN</role>
</ace>
<ace>
<action>write</action>
<allow>true</allow>
<role>ROLE_USER_ADMIN</role>
</ace>
<ace>
<action>read</action>
<allow>true</allow>
<role>ROLE_ANONYMOUS</role>
</ace>
</acl>'

###################################

for i in $(seq "$SERIES_SEQ"); do
SERIES_DATE="$(date -Iseconds)"

# opencast series dublincore catalog template
read -r -d '' SERIES_XML << EOM
<?xml version="1.0"?>
<dublincore xmlns="http://www.opencastproject.org/xsd/1.0/dublincore/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.opencastproject.org http://www.opencastproject.org/schema.xsd" xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:dcterms="http://purl.org/dc/terms/" xmlns:oc="http://www.opencastproject.org/matterhorn/">

  <dcterms:title xml:lang="en">
    Test Series #$i
  </dcterms:title>
  <dcterms:subject>
    Some Test Series
  </dcterms:subject>
  <dcterms:description xml:lang="en">
    Test Series #$i Description
  </dcterms:description>
  <dcterms:publisher>
    Publisher #$((i%10))
  </dcterms:publisher>
  <dcterms:modified xsi:type="dcterms:W3CDTF">
    $SERIES_DATE
  </dcterms:modified>
  <dcterms:format xsi:type="dcterms:IMT">
  </dcterms:format>
</dublincore>
EOM

curl -f -w "\\n" --digest -u $OC_DIGEST_USER:$OC_DIGEST_PASSWORD -H "X-Requested-Auth: Digest" \
  -X POST "$OC_URL/series/" \
  --data-urlencode "series=$SERIES_XML" \
  --data-urlencode "acl=$SERIES_ACL" &

PIDS[$((i%PARALlEL_PS))]="$!"
if [ "$((i%PARALlEL_PS))" -eq "0" ]; then
	for waitidx in $(seq 0 $((PARALlEL_PS-1))); do
		wait "${PIDS[$waitidx]}" >/dev/null 2>&1
	done
fi
done

# wait for running processes
for waitidx in $(seq 0 $((PARALlEL_PS-1))); do
	wait "${PIDS[$waitidx]}" >/dev/null 2>&1
done

echo "series range $SERIES_SEQ created"

