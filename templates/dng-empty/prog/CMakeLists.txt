# Dng Empty: a daNetGame game, built by python project.py build (the client, and the dedicated server in a tree with
# DAGOR_DEDICATED) into ../game/<platform>-<arch>. ../engine.blk names the engine checkout; DAGOR_ENGINE_ROOT
# overrides it.
cmake_minimum_required(VERSION 4.0)

if(NOT DAGOR_ENGINE_ROOT)
  file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/../engine.blk" _engine REGEX "^[ \t]*engineRoot[ \t]*:[ \t]*t[ \t]*=")
  if(NOT _engine MATCHES "\"([^\"]*)\"")
    message(FATAL_ERROR "engine.blk: expected engineRoot:t=\"<path to the engine checkout>\"")
  endif()
  string(REGEX REPLACE "~(.)" "\\1" _engine "${CMAKE_MATCH_1}") # ~ escapes in BLK strings
  cmake_path(ABSOLUTE_PATH _engine BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/.." NORMALIZE OUTPUT_VARIABLE _engine)
  set(DAGOR_ENGINE_ROOT "${_engine}")
  unset(_engine)
endif()
if(NOT EXISTS "${DAGOR_ENGINE_ROOT}/prog/cmake/DagorBootstrap.cmake")
  message(FATAL_ERROR "${DAGOR_ENGINE_ROOT} is not a Dagor Engine checkout with the CMake build; set engineRoot in "
                      "engine.blk (or DAGOR_ENGINE_ROOT) to the engine dir")
endif()
include("${DAGOR_ENGINE_ROOT}/prog/cmake/DagorBootstrap.cmake")
project(dng_empty LANGUAGES C CXX)
include(DagorEngine)

# the game, in a scope of its own: the engine dirs added at dagor_finalize() see none of its variables
block(SCOPE_FOR VARIABLES)
  dagor_glob_sources(das DIRS scripts/dng_empty scripts/dng_empty/es GLOB *.das) # compiled ahead of time with DAGOR_DAS_AOT

  set(sources)
  set(deps daNetGame daNetGameLibs.dm.stub)
  set(client OFF)
  if(NOT DAGOR_DEDICATED AND NOT DAGOR_DAS_AOT_COMPILER)
    set(client ON)
  endif()
  if(client AND WIN32)
    list(APPEND sources platform/windows/dng_empty.rc platform/windows/dng_empty.exe.manifest)
  elseif(client AND NOT CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
    message(FATAL_ERROR "dng_empty: the ${DAGOR_PLATFORM} client's packaging is not ported yet")
  endif()

  dagor_add_dng_game(dng_empty GAME dng_empty
    # the linux dedicated server checks the clients' auth keys (NetPeerAuth): zero keys let any linux client in, set
    # real ones before shipping; windows and macOS clients are not checked
    AUTH_KEY_LINUX 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    DEDICATED_AUTH linux linux
    CPP_DIRS main
    DNG_LIBS danetgamelibs.txt
    GAME_LIBS gamelibs.txt
    SOURCES ${sources}
    DAS_AOT ${das}
    AOT_SOURCES main/dasGameModulesList.cpp # the game's daScript modules, for its AOT compiler
    PRIVATE_INCLUDES ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs
    DEPS ${deps}
    OUTPUT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../game/${DAGOR_PLATFORM}-${DAGOR_ARCH}
  )

  if(client AND CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    # game/DngEmpty.app (DngEmptyArm64.app on arm64, as game/client.sh expects)
    set(bundle DngEmpty)
    if(DAGOR_ARCH STREQUAL "arm64")
      string(APPEND bundle Arm64)
    endif()
    dagor_apple_bundle(dng_empty NAME ${bundle} ID com.dagor.DngEmpty DIR ../game ICON platform/macOS/dng_empty.icns)
  endif()

  # python project.py package: the game with the data python project.py build made; -forcestart: the game has no
  # launcher (updater), which Windows release clients ask to be started by otherwise
  set(data content dng_empty.vromfs.bin)
  if(NOT DAGOR_DEDICATED)
    list(APPEND data compiledShaders)
  endif()
  dagor_package_game(dng_empty GAME_DIR ../game DATA ${data} ARGS -forcestart)

  # python project.py build shaders vromfs tools assets: the game's content, made by the client's tree with the
  # engine's tools (targets shaders, vromfs, tools, assets): the game's shaders into ../game/compiledShaders, those of
  # the tools (daEditor, daViewer, dabuild, impostorBaker) into ../tools, their intermediate files into the build dir
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
    elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
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
  endif()
endblock()

add_subdirectory(tests)

dagor_finalize()
