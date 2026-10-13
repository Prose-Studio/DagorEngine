#!/usr/bin/env bash
# dabuild: exports assets/ into the game packs (../game/content), as the content target of the client tree does
cd "$(dirname "$0")" || exit 1
. ../_engine.sh || { echo "Configure the project first: cmake --preset <host>-client in prog"; exit 1; }
exec "$DAGOR_CDK_DIR/daBuild-dev" ../application.blk -q -jobs:$(getconf _NPROCESSORS_ONLN) "$@"
