#!/bin/sh

set -e

RUN_WORKFLOWS_AT_ONCE=10
WAIT_SEC_IN_BETWEEN=60

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

if [ "x" != "x$PROPERTIES" ]; then
    for p in "${PROPERTIES[@]}"; do
        ARGS+=" -W $p"
    done
fi

if [ "x" != "x$OC_SERVER_URL" ]; then
    ARGS+=" -o $OC_SERVER_URL"
fi

if [ "x" != "x$OC_USER" ]; then
    ARGS+=" -u $OC_USER"
fi

if [ "x" != "x$OC_PASSWORD" ]; then
    ARGS+=" -p $OC_PASSWORD"
fi

echo "Please enter one media package id per line (an empty line will exit this program):"
c=0
while IFS= read -r mp; do
    [ "x" == "x$mp" ]  && exit 0
    echo "Start workflow on media package $mp"
    python3 StartWorkflow.py -m $mp $ARGS || /bin/true
    c=$((c+1))
    if [ 0 -eq $((c%RUN_WORKFLOWS_AT_ONCE)) ] && [ 0 -lt $WAIT_SEC_IN_BETWEEN ]; then
        echo "Wait ${WAIT_SEC_IN_BETWEEN}sec..."
        sleep $WAIT_SEC_IN_BETWEEN
    fi
done