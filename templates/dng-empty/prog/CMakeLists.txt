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
  set(deps daNetGame daNetGameLibs/dm/stub)
  if(NOT DAGOR_DEDICATED AND DAGOR_PLATFORM STREQUAL "windows")
    list(APPEND sources platform/windows/dng_empty.rc platform/windows/dng_empty.exe.manifest)
  elseif(NOT DAGOR_DEDICATED AND NOT DAGOR_DAS_AOT_COMPILER AND NOT DAGOR_PLATFORM STREQUAL "linux")
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

  # python project.py package: the game with the data python project.py build made; -forcestart: the game has no
  # launcher (updater), which Windows release clients ask to be started by otherwise
  set(data content dng_empty.vromfs.bin)
  if(NOT DAGOR_DEDICATED)
    list(APPEND data compiledShaders)
  endif()
  dagor_package_game(dng_empty GAME_DIR ../game DATA ${data} ARGS -forcestart)
endblock()

add_subdirectory(tests)

dagor_finalize()
