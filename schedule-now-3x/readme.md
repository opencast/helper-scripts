Schedule 1min Event in 1min
===========================

By default, this script will schedule a one minute test reconding in one
minute. Capture agent and server can be specified at the top of the script:

- `CAPTURE_AGENT="pyca"`
- `SERVER="https://octestallinone.virtuos.uos.de"`
- `USER="opencast_system_account"`
- `PASSWORD="CHANGE_ME"`

The default times can be passed to the script as command line argument. For
example, to schedule a 15min recording in 5 min run:

    sh schedule-now.sh 5 15

A more complex example: To schedule 100 recordings of 5 minutes each, starting
in 1 minute, and at 15 minute intervals after that:

for i in {0..100}; do sh schedule-now.sh $((15 * i + 1)) 5; done
