# Starter Game: a multiplayer daNetGame game. Configure, build, test and package it with the presets of
# CMakePresets.json (cmake --list-presets): the client (<host>-client) and the dedicated server (<host>-dedicated) go to
# ../game/<platform>-<arch>; the client's tree also makes the game's content into ../game (target content: shaders,
# vromfs, the daEditor snapshot, assets). The engine comes from find_package(Dagor), which the presets point at it.
cmake_minimum_required(VERSION 4.0)
project(starter_game LANGUAGES C CXX)
find_package(Dagor REQUIRED)

# the game program; in the tree of its daScript AOT compiler, the compiler (with the game's own daScript modules)
dagor_add_dng_game(NAME starter_game GAME starter_game
  # the linux dedicated server checks the clients' auth keys (NetPeerAuth): zero keys let any linux client in, set
  # real ones before shipping; windows and macOS clients are not checked
  AUTH_KEY_LINUX 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
  DEDICATED_AUTH linux linux
  DNG_LIBS danetgamelibs.txt
  GAME_LIBS gamelibs.txt
  FILES_CMAKE starter_game_files.cmake
  AOT_FILES_CMAKE starter_game_aot_files.cmake
  OUTPUT_DIRECTORY ../game/${DAGOR_PLATFORM}-${DAGOR_ARCH}
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs
  BUILD_DEPENDENCIES PRIVATE daNetGameLibs.dm.stub
  DAS_PULL starter_game_DAS_pull_AOT
)
if(DAGOR_DAS_AOT_COMPILER)
  return()
endif()

# the UI fonts' license (gameBase/ui), in the game's LICENSE-starter_game
dagor_target_licenses(starter_game ${CMAKE_CURRENT_SOURCE_DIR}/gameBase/ui/OFL-1.1.txt)

if(APPLE AND NOT DAGOR_DEDICATED)
  # the app bundle in ../game, where it finds the game's data (<bundle>/Contents/MacOS/../../..)
  dagor_apple_bundle(starter_game NAME StarterGame ID com.example.StarterGame ICON platform/macOS/starter_game.icns)
  dagor_set_output_directory(starter_game "${CMAKE_CURRENT_SOURCE_DIR}/../game")
endif()

# the packages (cpack --preset): the client, or the dedicated server, with the content the client's tree made;
# -forcestart: the game has no launcher (updater), which Windows release clients ask to be started by otherwise
if(DAGOR_DEDICATED)
  dagor_package_game(starter_game GAME_DIR ../game DATA content starter_game.vromfs.bin ARGS -forcestart)
else()
  dagor_package_game(starter_game GAME_DIR ../game DATA content starter_game.vromfs.bin compiledShaders ARGS -forcestart)
  dagor_add_dng_content(GAME_DIR ../game)
endif()

add_subdirectory(tests)
