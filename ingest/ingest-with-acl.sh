#!/bin/bash

set -eux

HOST="https://develop.opencast.org"
USER="admin"
PASSWORD="opencast"
WORKFLOW='fast'

TMP_MP="$(mktemp --suffix=.xml)"
TMP_DC="$(mktemp --suffix=.xml)"
TMP_ACL="$(mktemp --suffix=.xml)"
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
  <dcterms:language>eng</dcterms:language>
  <dcterms:spatial>pyca</dcterms:spatial>
  <dcterms:title>Demo event</dcterms:title>
</dublincore>' > "${TMP_DC}"

echo '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Policy PolicyId="mediapackage-1"
  RuleCombiningAlgId="urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:permit-overrides"
  Version="2.0"
  xmlns="urn:oasis:names:tc:xacml:2.0:policy:schema:os">
  <Rule RuleId="CA_User_read_Permit" Effect="Permit">
    <Target>
      <Actions>
        <Action>
          <ActionMatch MatchId="urn:oasis:names:tc:xacml:1.0:function:string-equal">
            <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">read</AttributeValue>
            <ActionAttributeDesignator AttributeId="urn:oasis:names:tc:xacml:1.0:action:action-id"
              DataType="http://www.w3.org/2001/XMLSchema#string"/>
          </ActionMatch>
        </Action>
      </Actions>
    </Target>
    <Condition>
      <Apply FunctionId="urn:oasis:names:tc:xacml:1.0:function:string-is-in">
        <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">ROLE_CAPTURE_AGENT</AttributeValue>
        <SubjectAttributeDesignator AttributeId="urn:oasis:names:tc:xacml:2.0:subject:role"
          DataType="http://www.w3.org/2001/XMLSchema#string"/>
      </Apply>
    </Condition>
  </Rule>
  <Rule RuleId="CA_User_write_Permit" Effect="Permit">
    <Target>
      <Actions>
        <Action>
          <ActionMatch MatchId="urn:oasis:names:tc:xacml:1.0:function:string-equal">
            <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">write</AttributeValue>
            <ActionAttributeDesignator AttributeId="urn:oasis:names:tc:xacml:1.0:action:action-id"
              DataType="http://www.w3.org/2001/XMLSchema#string"/>
          </ActionMatch>
        </Action>
      </Actions>
    </Target>
    <Condition>
      <Apply FunctionId="urn:oasis:names:tc:xacml:1.0:function:string-is-in">
        <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">ROLE_CAPTURE_AGENT</AttributeValue>
        <SubjectAttributeDesignator AttributeId="urn:oasis:names:tc:xacml:2.0:subject:role"
          DataType="http://www.w3.org/2001/XMLSchema#string"/>
      </Apply>
    </Condition>
  </Rule>
</Policy>' > "${TMP_ACL}"

# Create media package
curl -f -u ${USER}:${PASSWORD} \
  "${HOST}/ingest/createMediaPackage" -o "${TMP_MP}"

# Add DC catalog
curl -f -u ${USER}:${PASSWORD} \
  "${HOST}/ingest/addDCCatalog" -F "mediaPackage=<${TMP_MP}" \
  -F "dublinCore=<${TMP_DC}" -o "${TMP_MP}"

# Add ACL
curl -f -u ${USER}:${PASSWORD} \
  "${HOST}/ingest/addAttachment" -F "mediaPackage=<${TMP_MP}" \
  -F 'flavor=security/xacml+episode' -F "BODY=@${TMP_ACL}" -o "${TMP_MP}"

# Add Track
curl -f -u ${USER}:${PASSWORD} \
  "${HOST}/ingest/addTrack" -F flavor=presenter/source \
  -F "mediaPackage=<${TMP_MP}" -F Body=@video.webm -o "${TMP_MP}"

# Add Track
curl -f -u ${USER}:${PASSWORD} \
  "${HOST}/ingest/addTrack" -F flavor=presentation/source \
  -F "mediaPackage=<${TMP_MP}" -F Body=@video.webm -o "${TMP_MP}"

curl -f -u ${USER}:${PASSWORD} \
    "${HOST}/ingest/ingest/${WORKFLOW}" \
	 --data-urlencode "mediaPackage=$(cat "${TMP_MP}")"

rm -f "${TMP_MP}" "${TMP_DC}" "${TMP_ACL}"
