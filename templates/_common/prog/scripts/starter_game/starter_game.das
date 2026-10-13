options gen2
options no_aot = true // a loader: the scripts it loads are compiled ahead of time (DAS_FILES of starter_game_files.cmake)
require app
require ecs.fs
require DngNet
require %scripts/_libs_init // load_libs(): the libs in prog/danetgamelibs.txt, written by the CMake configure

// The game's das entry point (settings.blk game_das_script:t=): loads every script of the game. Systems in es/ are
// loaded everywhere and say where they run with their tags ([es(tag=server)]: where the game state is simulated, the
// dedicated server or a game without one; tag=gameClient: where a player plays; tag=render, tag=input, ...); es/client/
// holds what only a player's game needs (presentation, UI, input), never loaded by a dedicated server.
[init]
def load {
  var ok = load_libs()
  ok = load_folder("%scripts/starter_game/es") && ok
  if (is_in_aot() || !is_dedicated()) { // is_in_aot() first: the AOT compiler has no is_dedicated()
    ok = load_optional_folder("%scripts/starter_game/es/client") && ok
  }
  if (is_in_aot()) {
    assert(ok)
  }
}
