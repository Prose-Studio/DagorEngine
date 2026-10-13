# Starter Game

A daNetGame game built with the Dagor Engine. `engineRoot` in `application.blk` names the engine checkout (relative
to this dir or absolute); the project can be anywhere. `python <engine>/dng.py relink <this dir>` points it at another checkout.

A single-player game is its own server: one program, `<host>-client`, runs every system. A multiplayer game is also
built as a dedicated server, `<host>-dedicated`, which players' clients join.

## Build and run

In `prog/` (`cmake --list-presets` lists the trees):

```bash
cmake --workflow --preset windows                  # everything: the game, its content (and its dedicated server)
cmake --workflow --preset windows-test             # the tests that need no GPU
cmake --preset windows-client                      # one tree at a time: the game
cmake --build --preset windows-client
cmake --build --preset windows-client-content      # its content: shaders, vromfs, editor snapshot, assets
cmake --preset windows-dedicated                   # multiplayer: the dedicated server
cmake --build --preset windows-dedicated
```

(`linux` and `macos` on those hosts.) The programs go to `game/<platform>-<arch>`, the content to `game/`; the trees
are in `build/`. The content is made with the engine's tools (shader compilers, vromfsPacker, daBuild), which the
engine's own trees build when they are missing or out of date.

```bash
game/client.cmd                                    # or game/client.sh: the game, on the scripts and data in prog/
game/server.cmd                                    # multiplayer: the dedicated server; join with client.cmd -connect:localhost
```

## Layout

```text
application.blk     the engine checkout (engineRoot) and the tools' setup (daEditor, daViewer, dabuild, impostorBaker)
develop/            tool scripts (daEditor, daViewer, dabuild, daImpostor), assets/ and levels/
game/               what ships: executables, compiledShaders, vromfs, content (all built), run scripts
prog/
  CMakeLists.txt    the game: its program, content, package and tests
  CMakePresets.json its trees on the engine's presets (written by dng.py new and relink)
  danetgamelibs.txt engine libs the game uses (prog/daNetGameLibs), gamelibs.txt likewise for prog/gameLibs
  prog.vromfs.blk   what goes into game/starter_game.vromfs.bin
  main/             the game's C++ (das modules it adds)
  gameBase/         settings, scenes, entity templates
  scripts/          das scripts: starter_game/starter_game.das loads everything else
  shaders/          shader setup; source/ holds the game's hooks into the renderer
  tools/            what daEditor runs of the game
  tests/            cpp, das, ecs and scenario tests
```

Files starting with `_` (`_engine.cmd`, `prog/_libs*`, ...) are written by the CMake configure from the engine path and
the lib lists; they are not committed.

## Scripts

`scripts/starter_game/starter_game.das` loads the game's systems: `es/` everywhere, each system saying where it runs
with its tags (`[es(tag=server)]` where the game state is simulated: the dedicated server, or a single-player game;
`tag=gameClient` where a player plays; `tag=render`, `tag=input`, ...), and `es/client/` with what only a player's game
needs (presentation, UI, input), which a dedicated server never loads.

## Libraries

Add or remove engine libs in `prog/danetgamelibs.txt` (and `prog/gamelibs.txt`), then configure: it rewrites the vromfs,
template, das and shader lists for them. Libs with an `_init.das` are loaded by `load_libs()` in
`scripts/starter_game/starter_game.das`; some need their entity templates created by a scene (see the lib's
`templates/`).

## Tests

```bash
ctest --preset windows-dedicated                   # multiplayer: cpp, das and ecs tests
ctest --preset windows-client                      # the scenario tests (single-player: every test)
ctest --preset windows-client -L ecs               # one layer
ctest --preset windows-client -R starter_game.ecs -V
```

| Dir | Layer | What |
|---|---|---|
| `prog/tests/cpp` | cpp | Catch2 tests of C++ code and data files |
| `prog/tests/das` | das | dastest tests of pure das logic, no game needed |
| `prog/tests/ecs` | ecs | `[ecs_test]` functions in the game (the dedicated server, or the single-player game headless): entities, systems, frames |
| `prog/tests/scenarios` | scenario | `[ecs_test]` functions in the client: input, rendering, screenshots |

`prog/tests/CMakeLists.txt` says which tree runs which. Results and screenshots go to
`build/<preset>/test-artifacts/`. See `<engine>/_docs/source/testing`.

## Packages

`cmake --workflow --preset windows-client-package` (and `windows-dedicated-package`) builds the program in Rel and
packs it with the game's data into `build/<preset>/packages/` (a zip on Windows, a .tar.gz elsewhere): the program and
its DLLs in `<platform>-<arch>/`, the shaders, vromfs and content, and a launcher. Build the content first.
`dagor_package_game()` in `prog/CMakeLists.txt` lists what goes in.

## Assets

`develop/assets` holds the game's source assets; the content target (or `develop/dabuild`) exports them into packs in
`game/content/starter_game/res`, which the game loads (settings.blk `addons{}`). `.folder.blk` there holds the export
rules. `develop/assets/base` has placeholders for the textures the renderer looks up by name (stars, moon, strata
clouds, the paint palette): replace them with real art under the same names.

## Tools

`develop/daEditor` opens the editor on this project; levels go to `develop/levels`. `develop/daViewer` browses the
assets in `develop/assets`, `develop/dabuild` exports them into the game. The editor renders levels with the game's
renderer: build the content after changing shaders, scripts or game data so its snapshot (`tools/snapshot`) is current.
