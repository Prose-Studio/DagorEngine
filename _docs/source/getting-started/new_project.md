# Creating a Project

`dng.py new` in the engine root creates a game project from a template in `templates/`. The project can live
anywhere: `engineRoot` in its `application.blk` names the engine checkout it is built with, and its `prog/CMakePresets.json` includes the
engine's presets, so the build, the game and the tools find the engine wherever both are.

```bash
python dng.py new --template sp-3d --name MyGame --dest ../MyGame
cd ../MyGame/prog
cmake --workflow --preset windows            # everything: the game, its content, the engine tools it needs
cmake --workflow --preset windows-test       # the tests that need no GPU
../game/client.cmd
```

## Templates

`python dng.py new --list` shows them. Every template is a daNetGame game with the scripts of the tools (daEditor,
daViewer, dabuild, daImpostor), one sample entity system and a test target of every
[test layer](../testing/overview.md); its `README.md` describes the layout.

| Template | Game |
|---|---|
| `sp-3d` | single-player 3D: the game is its own server; the default world (sky and light, no level data) through a perspective camera |
| `mp-3d` | multiplayer 3D: a client and a dedicated server; the same world |
| `sp-2d` | single-player 2D: a world in the XY plane through an orthographic camera (`ortho_cam`, `camera__orthoHeight`) |
| `mp-2d` | multiplayer 2D: a client and a dedicated server; the same world |

A single-player game builds one program (`<host>-client`) that runs every system, its ECS tests headless on the stub
driver where the tree has it. A multiplayer game also builds the dedicated server (`<host>-dedicated`), which runs the
simulation (`[es(tag=server)]` systems) for the clients that join it; in both, `scripts/<codename>/es/client/` holds
what only a player's game loads.

The templates are made of layers, dirs starting with `_` that are not templates themselves: `_common` (what every game
has), `_singleplayer` or `_multiplayer` (the CMakeLists, test trees, the server's run scripts) and `_2d` or `_3d` (the
scenes). A template's `template.blk` lists its layers in order; each layer's files replace those of the layers before
it, and the template dir's own files come last. `_common/template.blk` lists the name tokens the layers use
(`starter_game`, `StarterGame`, `Starter Game`, `com.example.StarterGame`); the generator replaces them in file names and
text files, and refuses to finish if one is left. CI creates a project from every template and builds, tests and
packages it (`.github/workflows/template.yaml`).

The templates are under the engine's license, like `prog/`. They take nothing from Gaijin's downloadable sample content,
which is licensed differently: the textures the renderer needs by name (stars, moon, strata clouds, a paint palette)
are generated placeholders in `develop/assets/base` to be replaced, and water, glass scratches, fluid wind and UI fonts
are off until a game brings their assets (see `gameparams.blk` and `settings.blk`).

## Options

| Option | Meaning |
|---|---|
| `--template` | template id (`--list` shows them; default `mp-3d`) |
| `--name` | PascalCase name (`MyGame`): macOS bundle and Windows manifest names |
| `--codename` | lowercase name of the executables, the main vromfs and script dirs (default from `--name`: `my_game`) |
| `--title` | human readable name: window title, executable info (default from `--name`: `My Game`) |
| `--company` | reverse domain name for the bundle id `<company>.<name>` (default `com.example`) |
| `--dest` | the project dir: new or empty, ASCII without spaces (default `../<name>` next to the engine) |
| `--absolute-engine-path` | `application.blk` and the presets store an absolute path (by default relative, absolute only across drives) |
| `--no-git` | no `git init` in the new project |
| `--dry-run` | print the files it would create |

The game's content (shaders, vromfs, the editor snapshot, assets) is made with the engine's tools, which the
project's client tree builds in the engine's own trees when they are missing or out of date.

## Linking a project to an engine

```text
engineRoot:t="../DagorEngine"   // application.blk: relative to the project, or absolute
```

`python <engine>/dng.py relink <project dir>` points `engineRoot` and `prog/CMakePresets.json` at that engine (after
either moved). The CMake configure writes the files that depend on the engine and the lib lists; they are not
committed:

| Generated file | For |
|---|---|
| `_engine.cmd`, `_engine.sh` | the develop scripts: `DAGOR_ENGINE_ROOT` and `DAGOR_CDK_DIR` |
| `prog/_libs*` | the libs of `prog/danetgamelibs.txt` and `prog/gamelibs.txt`: vromfs, templates, das init, shaders |

Inside the engine, data files name engine paths through the `%engine` named mount, which the engine resolves from
`engineRoot` too (from the first project `application.blk` or engine checkout above the current dir, unless the `DAGOR_ENGINE_ROOT`
environment variable names one): settings `mountPoints`, shader and vromfs configs and `application.blk` use
`%engine/prog/...` and work wherever the project is.
