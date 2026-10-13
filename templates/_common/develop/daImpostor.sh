#!/usr/bin/env bash
# impostorBaker: bakes impostor textures of the assets that use them
cd "$(dirname "$0")" || exit 1
. ../_engine.sh || { echo "Configure the project first: cmake --preset <host>-client in prog"; exit 1; }
exec "$DAGOR_CDK_DIR/impostorBaker-dev" ../application.blk -rootdir:./ -clean:yes "$@"
