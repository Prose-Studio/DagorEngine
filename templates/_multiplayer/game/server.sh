#!/usr/bin/env bash
# Runs the dedicated server on port 2992 (clients join with client.sh -connect:localhost); scripts are read from ../prog
cd "$(dirname "$0")" || exit 1
case "$(uname -s)" in
  Darwin) exec ./macOS-$(uname -m)/starter_game-ded-dev -config:debug/useAddonVromSrc:b=yes -listen:0.0.0.0:2992 "$@" ;;
  *)      exec ./linux-$(uname -m)/starter_game-ded-dev -config:debug/useAddonVromSrc:b=yes -listen:0.0.0.0:2992 "$@" ;;
esac
