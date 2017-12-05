DIGEST_LOGIN='opencast_system_account:CHANGE_ME'
PERIOD='2017-08-01T00:00:00.000Z/2017-11-27T00:00:00.000Z'
FILENAME='events.json'

curl -f -i --digest -o ${FILENAME} -u ${DIGEST_LOGIN} -H "X-Requested-Auth: Digest" http://oc-admin.virtuos.uos.de/admin-ng/event/events.json?filter=technical_start:${PERIOD}&sort=createdDateTime:DESC

