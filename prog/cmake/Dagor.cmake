# The engine's build: included after project() by the top-level CMakeLists.txt, the engine's own (prog/CMakeLists.txt)
# or a project's through find_package(Dagor) (DagorConfig.cmake). The toolchain comes from the preset
# (prog/CMakePresets.json, prog/cmake/presets): it sets the configurations and the target arch before project().
#
# It sets the tree-wide options (DagorOptions.cmake) and the compile and link settings of every target below the
# calling directory (DagorCompilerFlags.cmake), and loads the functions the CMakeLists of the engine and of projects
# use: dagor_add_library() and dagor_add_executable() (DagorTargets.cmake), the generated sources, daScript AOT, content,
# tests and packages.
include_guard(GLOBAL)

if(NOT DEFINED PROJECT_NAME)
  message(FATAL_ERROR "include(Dagor) comes after project()")
endif()
if(NOT CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
  message(FATAL_ERROR "include(Dagor) belongs in the top-level CMakeLists.txt (its settings apply to the dirs below it)")
endif()
if(NOT CMAKE_CXX_COMPILER_LOADED)
  message(FATAL_ERROR "The project() of a Dagor build must enable CXX (and C)")
endif()
if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE MATCHES "^(Dev|Rel|IRel|Dbg)$")
  message(FATAL_ERROR "Configure with a preset (cmake --preset <name>, see CMakePresets.json): the Dagor toolchains set "
                      "the configurations Dev, Rel, IRel and Dbg")
endif()

cmake_path(GET CMAKE_CURRENT_LIST_DIR PARENT_PATH DAGOR_PROG_DIR) # prog/cmake -> prog
cmake_path(GET DAGOR_PROG_DIR PARENT_PATH DAGOR_ENGINE_ROOT)
set(DAGOR_CMAKE_DIR "${CMAKE_CURRENT_LIST_DIR}")
list(PREPEND CMAKE_MODULE_PATH "${DAGOR_CMAKE_DIR}" "${DAGOR_CMAKE_DIR}/find")
if(NOT DAGOR_DEPS_DIR)
  message(FATAL_ERROR "DAGOR_DEPS_DIR is not set: configure with a preset, whose toolchain file sets it")
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# a link item that could name a target must name one: a misspelled library is a configure error, not '-lengine.mth'.
# System libraries are imported targets (System::<name>, DagorSystemLibs.cmake).
set(CMAKE_LINK_LIBRARIES_ONLY_TARGETS ON)
# the objects of Windows builds under hashed dir and file names: the dirs of a project tree are deep enough for the
# full names to pass MAX_PATH
if(CMAKE_HOST_WIN32)
  set(CMAKE_INTERMEDIATE_DIR_STRATEGY SHORT)
endif()

include(DagorHost)
include(DagorFetch)
include(DagorPlatform)
include(DagorOptions)
include(DagorPython)
include(DagorSystemLibs)
include(DagorCompilerFlags)
include(DagorTargets)
include(DagorLicenses)
include(DagorCodegen)
include(DagorHostTools)
include(DagorContent)
include(DagorDas)
include(DagorPhys)
include(DagorGame)
include(DagorTesting)
include(DagorPackaging)

message(STATUS "Dagor: ${DAGOR_PLATFORM}-${DAGOR_ARCH} ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}, "
               "variant ${DAGOR_VARIANT}, deps cache ${DAGOR_DEPS_DIR}")
