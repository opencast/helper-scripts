#!/bin/bash

set -eux

HOST="http://127.0.0.1:8080"

if [ $# -ge 1 ]; then
  HOST=$1
fi

USER="opencast_system_account"
PASSWORD="CHANGE_ME"
WORKFLOW='partial-import-test'

if [ $# -ge 2 ]; then
  WORKFLOW=$2
fi

# v = video, a = audio, p = presenter, s = presentation (s like slides)
# ap = audio presenter
# vap = video + audio presenter
# vp and vas = video presenter and video + audio presentation

# go through all combinations

. ./ap.sh
. ./ap-and-as.sh
. ./ap-and-vs.sh
. ./ap-and-vas.sh

. ./vp.sh
. ./vp-and-as.sh
. ./vp-and-vs.sh
. ./vp-and-vas.sh

. ./vap.sh
. ./vap-and-as.sh
. ./vap-and-vs.sh
. ./vap-and-vas.sh

. ./as.sh
. ./vs.sh
. ./vas.sh
