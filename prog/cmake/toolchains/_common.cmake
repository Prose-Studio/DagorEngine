# Shared by the toolchain files, which presets select (prog/cmake/presets/base.json). It settles what the engine needs
# before the first project() call: the target arch (DAGOR_ARCH, the host's by default), the per-user deps cache
# (DAGOR_DEPS_DIR), the build configurations and the flag overrides.
#
# A toolchain file runs again for every try_compile project, where the main project's cache is not visible: the values
# reach those projects through CMAKE_TRY_COMPILE_PLATFORM_VARIABLES.
cmake_path(GET CMAKE_CURRENT_LIST_DIR PARENT_PATH _dagor_cmake_dir)
include("${_dagor_cmake_dir}/DagorHost.cmake")
include("${_dagor_cmake_dir}/DagorFetch.cmake")
unset(_dagor_cmake_dir)

# dagor_toolchain_forward(<var>...): makes the values visible to the try_compile projects
macro(dagor_toolchain_forward)
  list(APPEND CMAKE_TRY_COMPILE_PLATFORM_VARIABLES ${ARGN})
  list(REMOVE_DUPLICATES CMAKE_TRY_COMPILE_PLATFORM_VARIABLES)
endmacro()

set(DAGOR_ARCH "${DAGOR_HOST_ARCH}" CACHE STRING "Target architecture: x86_64, arm64, e2k, universal (macOS)")

# the per-user cache of fetched SDKs, toolchains and the codegen venv, shared by every clone, worktree and project
if(NOT DAGOR_DEPS_DIR)
  if(DEFINED ENV{DAGOR_DEPS_DIR} AND NOT "$ENV{DAGOR_DEPS_DIR}" STREQUAL "")
    set(_dagor_deps "$ENV{DAGOR_DEPS_DIR}")
  elseif(CMAKE_HOST_WIN32)
    set(_dagor_deps "$ENV{LOCALAPPDATA}/dagor")
  elseif(CMAKE_HOST_APPLE)
    set(_dagor_deps "$ENV{HOME}/Library/Caches/dagor")
  elseif(DEFINED ENV{XDG_CACHE_HOME} AND NOT "$ENV{XDG_CACHE_HOME}" STREQUAL "")
    set(_dagor_deps "$ENV{XDG_CACHE_HOME}/dagor")
  else()
    set(_dagor_deps "$ENV{HOME}/.cache/dagor")
  endif()
  file(TO_CMAKE_PATH "${_dagor_deps}" _dagor_deps)
  set(DAGOR_DEPS_DIR "${_dagor_deps}" CACHE PATH "Cache of fetched SDKs, toolchains and the codegen Python venv")
  unset(_dagor_deps)
endif()
dagor_toolchain_forward(DAGOR_ARCH DAGOR_DEPS_DIR)

# the compiler cache: DAGOR_COMPILER_LAUNCHER (of the preset or of the environment) is sccache, the pinned one fetched
# into DAGOR_DEPS_DIR, or the path of another launcher (ccache); it is CMAKE_<LANG>_COMPILER_LAUNCHER unless that is set
if(NOT DEFINED DAGOR_COMPILER_LAUNCHER AND DEFINED ENV{DAGOR_COMPILER_LAUNCHER})
  set(DAGOR_COMPILER_LAUNCHER "$ENV{DAGOR_COMPILER_LAUNCHER}")
endif()
set(DAGOR_COMPILER_LAUNCHER "${DAGOR_COMPILER_LAUNCHER}" CACHE STRING
  "Compiler cache: sccache (the pinned one) or the path of a compiler launcher")
if(DAGOR_COMPILER_LAUNCHER AND NOT CMAKE_CXX_COMPILER_LAUNCHER)
  set(_dagor_launcher "${DAGOR_COMPILER_LAUNCHER}")
  if(_dagor_launcher STREQUAL "sccache")
    dagor_fetch_sdk(sccache _dagor_launcher)
    string(APPEND _dagor_launcher "/sccache")
    if(CMAKE_HOST_WIN32)
      string(APPEND _dagor_launcher ".exe")
    endif()
  endif()
  foreach(_dagor_lang C CXX OBJC OBJCXX)
    set(CMAKE_${_dagor_lang}_COMPILER_LAUNCHER "${_dagor_launcher}" CACHE STRING "The compiler cache (DAGOR_COMPILER_LAUNCHER)")
  endforeach()
  unset(_dagor_lang)
  unset(_dagor_launcher)
endif()
dagor_toolchain_forward(CMAKE_C_COMPILER_LAUNCHER CMAKE_CXX_COMPILER_LAUNCHER)

# dev (DAGOR_DBGLEVEL 1, optimized, logs and asserts), rel (0), irel (-1, no logs at all), dbg (2, unoptimized); the
# presets set them too (not in the try_compile projects, which have their own)
get_property(_dagor_try_compile GLOBAL PROPERTY IN_TRY_COMPILE)
if(NOT _dagor_try_compile)
  set(CMAKE_CONFIGURATION_TYPES Dev Rel IRel Dbg CACHE STRING "Build configurations")
  if(CMAKE_GENERATOR STREQUAL "Ninja Multi-Config") # the IDE generators reject the variable
    set(CMAKE_DEFAULT_BUILD_TYPE Dev CACHE STRING "Configuration of a plain cmake --build")
  endif()
  if(NOT CMAKE_GENERATOR MATCHES "Multi-Config|Visual Studio|Xcode" AND NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Dev CACHE STRING "Configuration of single-configuration generators: Dev, Rel, IRel or Dbg")
  endif()
endif()
unset(_dagor_try_compile)

# CMake's default flags (/GR /EHsc /W3 -O2 -g and the per-config ones) are replaced: the engine states every flag
# (DagorCompilerFlags.cmake), apart from those a toolchain needs for its compiler to work at all
# (DAGOR_TOOLCHAIN_<LANG>_FLAGS, DAGOR_TOOLCHAIN_LINKER_FLAGS)
set(CMAKE_USER_MAKE_RULES_OVERRIDE "${CMAKE_CURRENT_LIST_DIR}/flag-overrides.cmake")

# dagor_tool_version(<exe> <out-var>): the first x.y.z in the output of '<exe> --version'
function(dagor_tool_version exe out)
  execute_process(COMMAND "${exe}" --version OUTPUT_VARIABLE text ERROR_VARIABLE text RESULT_VARIABLE result)
  set(version "")
  if(result EQUAL 0 AND text MATCHES "([0-9]+\\.[0-9]+\\.[0-9]+)")
    set(version "${CMAKE_MATCH_1}")
  endif()
  set(${out} "${version}" PARENT_SCOPE)
endfunction()

# dagor_toolchain_llvm(): DAGOR_LLVM_DIR, an LLVM of the pinned version. An explicit -DDAGOR_LLVM_DIR wins; then an
# installed LLVM of that version (the official Windows installer's dir, or one on PATH); otherwise the release archive
# is fetched into the deps cache.
function(dagor_toolchain_llvm)
  dagor_sdk_version(llvm want)
  if(DAGOR_LLVM_DIR)
    set(dir "${DAGOR_LLVM_DIR}")
  else()
    set(dir "")
    set(candidates)
    if(CMAKE_HOST_WIN32)
      list(APPEND candidates "$ENV{ProgramFiles}/LLVM")
    endif()
    find_program(_dagor_clang_on_path NAMES clang NO_CACHE)
    if(_dagor_clang_on_path)
      cmake_path(GET _dagor_clang_on_path PARENT_PATH bin)
      cmake_path(GET bin PARENT_PATH root)
      list(APPEND candidates "${root}")
    endif()
    foreach(candidate IN LISTS candidates)
      file(TO_CMAKE_PATH "${candidate}" candidate)
      if(EXISTS "${candidate}/bin/clang${CMAKE_HOST_EXECUTABLE_SUFFIX}")
        dagor_tool_version("${candidate}/bin/clang${CMAKE_HOST_EXECUTABLE_SUFFIX}" have)
        if(have STREQUAL want)
          set(dir "${candidate}")
          break()
        endif()
      endif()
    endforeach()
    if(NOT dir)
      dagor_fetch_sdk(llvm dir)
    endif()
  endif()
  dagor_tool_version("${dir}/bin/clang${CMAKE_HOST_EXECUTABLE_SUFFIX}" have)
  if(NOT have STREQUAL want)
    message(FATAL_ERROR "DAGOR_LLVM_DIR='${dir}' is LLVM '${have}', the engine pins ${want}")
  endif()
  set(DAGOR_LLVM_DIR "${dir}" CACHE PATH "LLVM ${want} used by the build" FORCE)
  set(DAGOR_LLVM_VERSION "${want}" CACHE INTERNAL "")
endfunction()
