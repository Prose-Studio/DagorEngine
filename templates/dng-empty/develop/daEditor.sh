#!/usr/bin/env bash
# daEditor for this project (linux): its workspace is made from ../application.blk on the first start
cd "$(dirname "$0")" || exit 1
. ../_engine.sh || { echo "Configure the project first: cmake --preset <host>-client in prog"; exit 1; }
"$DAGOR_CDK_DIR/daEditor3x-dev" ../application.blk "$@" &
