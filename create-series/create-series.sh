#!/bin/bash

URL=http://localhost:8080
USER=admin
PASSWORD=opencast

curl -u "${USER}:${PASSWORD}" "${URL}/series/" \
	-F title="I 🖤 Opencast" \
	-F acl='{"acl": {"ace": [{"allow": true,"role": "ROLE_USER","action": "read"}]}}' \
	-F creator=lk
