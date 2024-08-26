#!/usr/bin/env bash

set -e

OUT_FILENAME="opencast-migration-scripts-$(date +%F).tar.gz"
git archive --prefix "opencast-migration-scripts/" -o "$OUT_FILENAME" HEAD
echo "Created archive: $OUT_FILENAME"
