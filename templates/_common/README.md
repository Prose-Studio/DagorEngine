# Starter Game

A daNetGame game built with the Dagor Engine. `engineRoot` in `application.blk` names the engine checkout (relative
to this dir or absolute); the project can be anywhere on the engine's drive.
`python3 <engine>/dagor.py relink <this dir>` points it at another checkout.

A single-player game is its own server: one program runs every system. A multiplayer game (`prog/dedicated.jam`
exists) is also built as a dedicated server, which players' clients join.

## Build and run

The engine's tools come first (once, and after engine updates): `python3 <engine>/dagor.py build project:dagorTools code`.
Then, here:

```bash
python3 prog/build.py                              # everything: the game (and its dedicated server) and its content
python3 prog/build.py code                         # the game only; shaders, gui (fonts), vromfs, assets: the content
python3 prog/build.py code arch:arm64              # another architecture
```

The programs go to `game/<platform>-<arch>`, the content to `game/`, the editor's files to `tools/`, the intermediate
files of the shaders to `build/`. In `prog/`, `jam` (after one `build.py` run) builds the game alone: `jam -sConfig=rel`
a release build, `jam -sDedicated=yes` the dedicated server.

```bash
game/client.cmd                                    # or game/client.sh: the game, on the scripts and data in prog/
game/server.cmd                                    # multiplayer: the dedicated server, on port 2992
game/client.cmd -connect:localhost                 # a client joining it (-connect:<host>[:<port>]; without it a local game)
```

## Layout

```text
application.blk     the engine checkout (engineRoot) and the tools' setup (daEditor, daViewer, dabuild, impostorBaker)
develop/            tool scripts (daEditor, daViewer, dabuild, daImpostor), assets/ and levels/
game/               what ships: executables, compiledShaders, vromfs, content (all built), run scripts
prog/
  build.py          builds the game and its content
  jamfile           the game program; jamfile-aot its daScript AOT compiler (aot_config.blk), dedicated.jam its server
  danetgamelibs.txt engine libs the game uses (prog/daNetGameLibs), gamelibs.txt likewise for prog/gameLibs
  prog.vromfs.blk   what goes into game/starter_game.vromfs.bin
  main/             the game's C++ (das modules it adds)
  gameBase/         settings, scenes, entity templates; ui/ the UI fonts
  scripts/          das scripts: starter_game/starter_game.das loads everything else; ui/ the overlay UI (daRg)
  shaders/          shader setup; source/ holds the game's hooks into the renderer
  tools/            what daEditor runs of the game
```

Files starting with `_` (`_engine.cmd`, `prog/_engine.jam`, `prog/_libs*`, ...) are written by `build.py` from the
engine path and the lib lists; they are not committed.

## Editor and UI

Outside Rel builds the game carries daNetGame's embedded editor: F12 opens and closes it (the scene's entities in an
outliner, select and move them, edit their components, create them from templates); Space in it toggles its camera.
F10 toggles the game's free camera. The editor is the engine's daRg UI (`prog/scripts/sq/daeditor`) in the game's
overlay UI, `prog/scripts/ui/ui.nut` (`ui/overlay_ui_script` of settings.blk), where the game's own UI goes too. Its
fonts are in `prog/gameBase/ui`: `fontgen.blk` names the `.ttf` files there (SIL Open Font License 1.1,
`OFL-1.1.txt`), and `build.py gui` makes `fonts.dynFont.blk` from it.

## Scripts

`scripts/starter_game/starter_game.das` loads the game's systems: `es/` everywhere, each system saying where it runs
with its tags (`[es(tag=server)]` where the game state is simulated: the dedicated server, or a single-player game;
`tag=gameClient` where a player plays; `tag=render`, `tag=input`, ...), and `es/client/` with what only a player's game
needs (presentation, UI, input), which a dedicated server never loads.

## Libraries

Add or remove engine libs in `prog/danetgamelibs.txt` (and `prog/gamelibs.txt`), then build: `build.py` rewrites the
jam, vromfs, template, das and shader lists for them. Libs with an `_init.das` are loaded by `load_libs()` in
`scripts/starter_game/starter_game.das`; some need their entity templates created by a scene (see the lib's
`templates/`).

## Assets

`develop/assets` holds the game's source assets; `build.py assets` (or `develop/dabuild`) exports them into packs in
`game/content/starter_game/res`, which the game loads (settings.blk `addons{}`). `.folder.blk` there holds the export
rules. `develop/assets/base` has placeholders for the textures the renderer looks up by name (stars, moon, strata
clouds, the paint palette): replace them with real art under the same names.

Hot reloading: the Windows game outside Rel builds in the asset manager (`assets_import` in `prog/gamelibs.txt`, the
`base_asset_manager` entity of `gamedata/scenes/_common_render_scene.blk`), which builds the assets the game loads from
`develop/assets` and rebuilds and reloads those that change while it runs: save a texture there and the game shows it;
rendInsts and animated characters (with the ecs anim library) reload too. Its debug window (ImGui) creates and inspects
assets. A release game reads the exported packs only.

## Tools

`develop/daEditor` opens the editor on this project; levels go to `develop/levels`. `develop/daViewer` browses the
assets in `develop/assets`, `develop/dabuild` exports them into the game. The editor renders levels with the game's
renderer: build the content after changing shaders, scripts or game data so its snapshot (`tools/snapshot`) is current.
