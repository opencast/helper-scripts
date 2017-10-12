Schedule 1min Event in 1min
===========================

*This script is for Opencast >= 4.0*

By default, this script will schedule a one minute test reconding in one
minute. Capture agent and server can be specified at the top of the script:

- `CAPTURE_AGENT="pyca"`
- `HOST="https://octestallinone.virtuos.uos.de"`
- `USER="opencast_system_account"`
- `PASSWORD="CHANGE_ME"`

The default times can be passed to the script as command line argument. For
example, to schedule a 15min recording in 5 min run:

    sh schedule-now.sh 5 15
