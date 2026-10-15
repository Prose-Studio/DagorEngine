# Making a Game Project

A game is a project of its own, made from one of the templates in
`DagorEngine/templates`. It can be anywhere on the engine's drive: its
`application.blk` names the engine it is built with (`engineRoot`), which its
build, the game and the tools all read.

| Template | Game |
|---|---|
| `sp-3d` | single-player 3D: the game is its own server; a 3D world with sky and light through a perspective camera |
| `mp-3d` | multiplayer 3D: a client and a dedicated server |
| `sp-2d` | single-player 2D: a world in the XY plane through an orthographic camera |
| `mp-2d` | multiplayer 2D |

All four are daNetGame games with the embedded editor (F12 in the game, outside
release builds), daEditor, daViewer and dabuild set up for the project, and no
content but placeholders.

## Create

The engine's tools come first, once and after engine updates:

```text
python3 dagor.py build project:dagorTools code
```

Then, in `DagorEngine`:

```text
python3 dagor.py new --template sp-3d --name MyGame
```

creates `../MyGame` (`--dest` names another dir, `--title` and `--codename`
other names than those made from `--name`, `--company` the reverse domain of
its bundle ids; `python3 dagor.py new --list` lists the templates).

## Build and run

```text
python3 ../MyGame/prog/build.py
../MyGame/game/client.cmd
```

`build.py` builds the game (and the dedicated server of a multiplayer game)
with jam and its content with the engine's tools: shaders, fonts, vromfs and
assets (`build.py code`, `shaders`, `gui`, `vromfs`, `assets` build one of
them). The project's `README.md` describes its layout, its libraries and its
tools.

## Move the engine or the project

```text
python3 dagor.py relink ../MyGame
```

points the project at this engine checkout: it rewrites `engineRoot` in its
`application.blk` and the files `build.py` writes from it (those starting with
`_`, which are not committed).
