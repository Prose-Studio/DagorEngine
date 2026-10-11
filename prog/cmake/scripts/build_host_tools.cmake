# cmake -DENGINE_ROOT=<engine> -DHOST_TAG=<host-arch> [-DVARIANT=cdk|editor] -DCONFIG=<config> -DTOOLS=<tool,...>
#       [-DDEPS_DIR=<dir>] [-DMAKE_PROGRAM=<ninja>] -P build_host_tools.cmake
# Builds the engine's host tools (see DagorHostTools.cmake): configures its cdk (or editor) tree for the host once
# (<engine>/build/<platform>-<variant>, the tree python dng.py build makes too), builds the tools (all of the editor
# tree: daBuild loads the plugins built with it) and installs them into <engine>/tools/dagor_cdk/<host>. A lock keeps
# the trees that share it from building it at the same time.
foreach(var ENGINE_ROOT HOST_TAG CONFIG TOOLS)
  if(NOT ${var})
    message(FATAL_ERROR "build_host_tools.cmake: ${var} is not set")
  endif()
endforeach()
string(REPLACE "," ";" TOOLS "${TOOLS}")
if(NOT VARIANT)
  set(VARIANT cdk)
endif()
# the tree python dng.py build <variant> makes for the host (pythonCommon/dagorCMake): build/<platform>-<variant>
string(REGEX REPLACE "-[^-]+$" "" platform "${HOST_TAG}")
string(TOLOWER "${platform}" platform)
set(tree "${ENGINE_ROOT}/build/${platform}-${VARIANT}")
file(MAKE_DIRECTORY "${ENGINE_ROOT}/build")
file(LOCK "${tree}.lock" TIMEOUT 14400 RESULT_VARIABLE locked)
if(locked)
  message(FATAL_ERROR "Cannot lock ${tree}.lock: ${locked}")
endif()

function(run)
  execute_process(COMMAND ${ARGN} RESULT_VARIABLE result)
  if(result)
    list(JOIN ARGN " " command)
    message(FATAL_ERROR "Host tools: '${command}' failed (${result})")
  endif()
endfunction()

# a tree configured for another source dir (the engine root before prog/CMakeLists.txt) is made anew
if(EXISTS "${tree}/CMakeCache.txt")
  file(STRINGS "${tree}/CMakeCache.txt" home REGEX "^CMAKE_HOME_DIRECTORY:INTERNAL=")
  string(REGEX REPLACE "^[^=]*=" "" home "${home}")
  cmake_path(COMPARE "${home}" EQUAL "${ENGINE_ROOT}/prog" same)
  if(NOT same)
    file(REMOVE_RECURSE "${tree}")
  endif()
endif()
if(NOT EXISTS "${tree}/CMakeCache.txt")
  set(args -S "${ENGINE_ROOT}/prog" -B "${tree}" -G "Ninja Multi-Config" -DDAGOR_VARIANT=${VARIANT}
    "-DCMAKE_INSTALL_PREFIX=${ENGINE_ROOT}")
  if(DEPS_DIR)
    list(APPEND args "-DDAGOR_DEPS_DIR=${DEPS_DIR}")
  endif()
  if(MAKE_PROGRAM)
    list(APPEND args "-DCMAKE_MAKE_PROGRAM=${MAKE_PROGRAM}")
  endif()
  run("${CMAKE_COMMAND}" ${args})
endif()
if(VARIANT STREQUAL "editor")
  run("${CMAKE_COMMAND}" --build "${tree}" --config "${CONFIG}")
else()
  run("${CMAKE_COMMAND}" --build "${tree}" --config "${CONFIG}" --target ${TOOLS})
endif()
run("${CMAKE_COMMAND}" --install "${tree}" --config "${CONFIG}" --component cdk)
