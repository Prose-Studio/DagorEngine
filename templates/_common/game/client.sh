#!/usr/bin/env bash
# Runs the game. The scripts and data are read from ../prog (no vromfs rebuild needed); pass more arguments as usual.
cd "$(dirname "$0")" || exit 1
if [ "$(uname -s)" = Darwin ]; then
  app=StarterGame; [ "$(uname -m)" = arm64 ] && app=StarterGameArm64
  exec "./$app.app/Contents/MacOS/starter_game-dev" -config:debug/useAddonVromSrc:b=yes "$@"
fi
exec "./linux-$(uname -m)/starter_game-dev" -config:debug/useAddonVromSrc:b=yes "$@"
