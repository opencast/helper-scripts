Schedule 1min Event in 1min
===========================

*This script is for Opencast >= 4.0*

By default, this script will schedule a one minute test reconding in one
minute. Capture agent and server can be specified at the top of the script:

- `CAPTURE_AGENT="pyca"`
- `HOST="https://octestallinone.virtuos.uos.de"`
- `USER="opencast_system_account"`
- `PASSWORD="CHANGE_ME"`

You can overwrite the default times be passed new ones to the script as command
line argument. For example, to schedule a 15min recording in 5 min run:

    ./schedule-now.sh 5 15

A more complex example: To schedule 100 recordings of 5 minutes each, starting
in 1 minute, and at 15 minute intervals after that (using bash):

    for i in {0..100}; do ./schedule-now.sh $((15 * i + 1)) 5; done
