#!/usr/bin/env bash
# daEditor for this project (linux): its workspace is made from ../application.blk on the first start
cd "$(dirname "$0")" || exit 1
. ../_engine.sh || { echo "Set the project up first: python3 prog/build.py"; exit 1; }
"$DAGOR_CDK_DIR/daEditor3x-dev" ../application.blk "$@" &
