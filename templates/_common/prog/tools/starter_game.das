options gen2
options no_aot = true
require ecs.fs
require %toolScripts/_libs_init // load_libs(): the libs in prog/danetgamelibs.txt, written by the CMake configure

// What daEditor runs to render levels like the game does (application.blk game{ daNetGameEditorRender:b=yes }): it
// replaces the game's entry script (settings.blk game_das_script:t=), so it loads only what the editor needs.
// the tools step of the client tree's content (cmake --build --preset <host>-client-content) copies this dir into the editor's snapshot (application.blk dngSnapshot:t=).
[init]
def load {
  load_libs()
  load_folder("%scripts/starter_game/es")
}
