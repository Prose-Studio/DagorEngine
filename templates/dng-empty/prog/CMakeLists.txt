# Dng Empty: a daNetGame game. Configure, build, test and package it with the presets of CMakePresets.json (cmake
# --list-presets): the client (<host>-client) and the dedicated server (<host>-dedicated) go to ../game/<platform>-<arch>;
# the client's tree also makes the game's content into ../game (target content: shaders, vromfs, the daEditor snapshot,
# assets). The engine comes from find_package(Dagor), which the presets point at it (Dagor_DIR).
cmake_minimum_required(VERSION 4.0)
project(dng_empty LANGUAGES C CXX)
find_package(Dagor REQUIRED)

set(sources)
set(client OFF)
if(NOT DAGOR_DEDICATED AND NOT DAGOR_DAS_AOT_COMPILER)
  set(client ON)
endif()
if(client AND WIN32)
  list(APPEND sources platform/windows/dng_empty.rc platform/windows/dng_empty.exe.manifest)
endif()

# the game program, in the tree of its daScript AOT compiler the compiler (with the game's own daScript modules)
dagor_add_dng_game(dng_empty GAME dng_empty
  # the linux dedicated server checks the clients' auth keys (NetPeerAuth): zero keys let any linux client in, set
  # real ones before shipping; windows and macOS clients are not checked
  AUTH_KEY_LINUX 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
  DEDICATED_AUTH linux linux
  CPP_DIRS main
  DNG_LIBS danetgamelibs.txt
  GAME_LIBS gamelibs.txt
  AOT_SOURCES main/dasGameModulesList.cpp
  OUTPUT_DIRECTORY ../game/${DAGOR_PLATFORM}-${DAGOR_ARCH}
  ${sources})
if(DAGOR_DAS_AOT_COMPILER)
  return()
endif()
target_include_directories(dng_empty PRIVATE ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs)
target_link_libraries(dng_empty PRIVATE daNetGame daNetGameLibs.dm.stub)
dagor_glob_sources(das DIRS scripts/dng_empty scripts/dng_empty/es GLOB *.das)
dagor_target_das_aot(dng_empty PULL dng_empty_DAS_pull_AOT ${das})

if(client AND CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  # the app bundle in ../game, where it finds the game's data (<bundle>/Contents/MacOS/../../..)
  dagor_apple_bundle(dng_empty NAME DngEmpty ID com.dagor.DngEmpty ICON platform/macOS/dng_empty.icns)
  dagor_set_output_directory(dng_empty "${CMAKE_CURRENT_SOURCE_DIR}/../game")
endif()

# the package (cpack --preset): the game with the content the client's tree made; -forcestart: the game has no
# launcher (updater), which Windows release clients ask to be started by otherwise
set(data content dng_empty.vromfs.bin)
if(client)
  list(APPEND data compiledShaders)
endif()
dagor_package_game(dng_empty GAME_DIR ../game DATA ${data} ARGS -forcestart)

# the game's content, made with the engine's tools (target content, or shaders, vromfs, tools, assets): the game's
# shaders into ../game/compiledShaders, those of the tools (daEditor, daViewer, dabuild, impostorBaker) into ../tools,
# their intermediate files into the build dir
if(client)
  # each step: <name>|<compiler>|<blk>|<arguments, | separated>
  set(dsc "-q|-shaderOn|-nodisassembly|-commentPP|-codeDumpErr|-maxVSF|4096")
  set(exp "-q|-shaderOn|-no_sha1_cache|-clearBlkHashInDump") # dabuild only needs the shader descriptions
  set(obj ${CMAKE_BINARY_DIR}/shaders)
  if(WIN32) # dx11 is the default driver and what daEditor renders levels with
    set(steps
      "game-dx11|dsc2-hlsl11|shaders_dx11.blk|${dsc}"
      "game-dx12|dsc2-dx12|shaders_dx12.blk|${dsc}|-wx"
      "tools-dx11|dsc2-hlsl11|shaders_tools11.blk|${dsc}"
      "impostorbaker-dx12|dsc2-dx12|shaders_impostorbaker.blk|${dsc}")
  elseif(APPLE)
    set(steps
      "game-metal|dsc2-metal|shaders_metal.blk|${dsc}"
      "tools-metal|dsc2-metal|shaders_tools11.blk|${dsc}|-out|../../tools/toolsMTL"
      "impostorbaker-metal|dsc2-metal|shaders_impostorbaker.blk|${dsc}|-out|../../tools/tools.impostorbakerMTL")
  else()
    set(steps
      "game-spirv|dsc2-spirv|shaders_spirv.blk|${dsc}"
      "tools-spirv|dsc2-spirv|shaders_tools11.blk|${dsc}|-out|../../tools/toolsSpirV"
      "impostorbaker-spirv|dsc2-spirv|shaders_impostorbaker.blk|${dsc}|-out|../../tools/tools.impostorbakerSpirV")
  endif()
  list(APPEND steps "tools-exp|dsc2-stub|shaders_tools_exp.blk|${exp}")
  foreach(step IN LISTS steps)
    string(REPLACE "|" ";" step "${step}")
    list(POP_FRONT step name tool blk)
    dagor_add_content_step(shaders-${name} TOOL ${tool} ARGS ${blk} ${step} -o ${obj}/${name}
      WORKING_DIRECTORY shaders GROUP shaders COMMENT "Shaders ${name} (${tool})")
  endforeach()
  # prog.vromfs.blk: ../game/dng_empty.vromfs.bin
  dagor_add_content_step(vromfs TOOL vromfsPacker ARGS prog.vromfs.blk -platform:PC -quiet -addpath:.
    COMMENT "The game's vromfs")
  # the snapshot of shaders, vromfs and tools/*.das daEditor renders levels with (../tools/snapshot)
  dagor_add_content_step(tools DEPENDS shaders vromfs COMMENT "The daEditor snapshot"
    COMMAND ${Python3_EXECUTABLE} -c "import glob, sys; sys.path.insert(0, sys.argv[1]); \
from update_dng_snapshots import update_dng_snapshot; \
update_dng_snapshot(sys.argv[2], 'game', glob.glob(sys.argv[2] + '/game/*.vromfs.bin'), skip_cvs_update=True)"
      ${DAGOR_PROG_DIR}/tools ${CMAKE_CURRENT_SOURCE_DIR}/..)
  # develop/assets with daBuild into ../game/content
  cmake_host_system_information(RESULT cores QUERY NUMBER_OF_LOGICAL_CORES)
  dagor_add_content_step(assets TOOL daBuild ARGS -jobs:${cores} -q ../application.blk WORKING_DIRECTORY ../develop
    COMMENT "The game's assets (daBuild)")
  add_custom_target(content DEPENDS shaders vromfs tools assets)
endif()

add_subdirectory(tests)
