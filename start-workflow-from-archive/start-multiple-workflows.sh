#!/bin/bash

set -e

RUN_WORKFLOWS_CONCURENTLY=10
START_WORKFLOWS_THRESHOLD=3


print_help() {
    echo "usage: $0 -w WORKFLOW [-W PROPERTIES] [-o OPENCAST] [-u USER] [-p PASSWORD] [-h]

required arguments:
  -w WORKFLOW, --workflow WORKFLOW
                        workflow definition identifier
optional arguments:
  -h, --help            show this help message and exit
  -W PROPERTIES, --properties PROPERTIES
                        workflow configuration properties (key=value)
  -o OPENCAST, --opencast OPENCAST
                        url of the opencast instance
  -u USER, --user USER  digest user name
  -p PASSWORD, --password PASSWORD
                        digest password"
}

if [ $# -eq 0 ]; then
    print_help
    exit 1
fi

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
    print_help
    exit 1
    ;;
    -w|--workflow)
    WORKFLOW="$2"
    shift # past argument
    shift # past value
    ;;
    -W|--properties)
    PROPERTIES+=(" $2")
    shift # past argument
    shift # past value
    ;;
    -o|--opencast)
    OC_SERVER_URL="$2"
    shift # past argument
    shift # past value
    ;;
    -u|--user)
    OC_USER="$2"
    shift # past argument
    shift # past value
    ;;
    -p|--password)
    OC_PASSWORD="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters


ARGS=""
if [ "x" == "x$WORKFLOW" ]; then
    echo "The workflow definition identifier is required. Please set it with the -w param."
    exit 1
else
    ARGS+=" -w $WORKFLOW"
fi

if [ -n "${PROPERTIES+x}" ]; then
    for p in "${PROPERTIES[@]}"; do
        ARGS+=" -W $p"
    done
fi

if [ "x" != "x$OC_SERVER_URL" ]; then
    ARGS+=" -o $OC_SERVER_URL"
elif [ -f "/etc/opencast/custom.properties" ]; then
    OC_SERVER_URL="$(grep -i '^org.opencastproject.server.url=.*$' /etc/opencast/custom.properties | cut -d'=' -f 2)"
else
    echo "Can't find the opencast configuration file /etc/opencast/custom.properties."
    echo "Please set the opencast server url."
    exit 1
fi

if [ "x" != "x$OC_USER" ]; then
    ARGS+=" -u $OC_USER"
elif [ -f "/etc/opencast/custom.properties" ]; then
    OC_USER="$(grep digest.user /etc/opencast/custom.properties | cut -d'=' -f 2)"
else
    echo "Can't find the opencast configuration file /etc/opencast/custom.properties."
    echo "Please set the opencast digest user."
    exit 1
fi

if [ "x" != "x$OC_PASSWORD" ]; then
    ARGS+=" -p $OC_PASSWORD"
elif [ -f "/etc/opencast/custom.properties" ]; then
    OC_PASSWORD="$(grep digest.pass /etc/opencast/custom.properties | cut -d'=' -f 2)"
else
    echo "Can't find the opencast configuration file /etc/opencast/custom.properties."
    echo "Please set the opencast digest user password."
    exit 1
fi

function get_active_workflows {
  active_workflows=$(curl --digest -u "$OC_USER:$OC_PASSWORD" -H "X-Requested-Auth: Digest" -s \
      "$OC_SERVER_URL/workflow/count?state=RUNNING")
  [ ! -z "${active_workflows##*[!0-9]*}" ] && echo "$active_workflows" || echo "999999"
}

function wait_active_workflows {
  [ "$(get_active_workflows)" -lt $RUN_WORKFLOWS_CONCURENTLY ] && return

  until [ "$(get_active_workflows)" -le $START_WORKFLOWS_THRESHOLD ]; do
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Wait for active workflows"
    sleep 5
  done
}

wait_active_workflows
echo "Please enter one media package id per line (an empty line will exit this program):"
while IFS= read -r mp; do
    [ "x" == "x$mp" ]  && exit 0
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Start workflow on media package $mp"
    # shellcheck disable=SC2086
    python3 start-workflow.py -m "$mp" $ARGS || true
    wait_active_workflows
done
