# The licenses of the libraries a program links, in the LICENSE-<program> file next to it (DagorTargets.cmake writes
# it from the program's DAGOR_LICENSE_FILES, a custom transitive property: the union over its link closure).
#
# A library's licenses are the license files of its directory (License.*, LICENSE*, COPYING*, COPYRIGHT, ...), or the
# LICENSES of its dagor_add_target(), plus those dagor_target_licenses() adds. A directory under 1stPartyLibs/ or 3rdPartyLibs/ that declares a target and has
# none fails the configure step, unless a NO_LICENSE file there says it needs none.
#
#   dagor_target_licenses(<target> <file or dir>...): more license files of <target> (a dir: its license files)
include_guard(GLOBAL)

set(_DAGOR_LICENSE_GLOBS License.* license.* LICENSE.* LICENSE_*.txt license LICENSE COPYING copying COPYING.*
  COPYRIGHT copyright)

# the license files of <dir>
function(_dagor_find_licenses dir out)
  set(patterns ${_DAGOR_LICENSE_GLOBS})
  list(TRANSFORM patterns PREPEND "${dir}/")
  file(GLOB found LIST_DIRECTORIES false ${patterns})
  list(SORT found)
  set(${out} "${found}" PARENT_SCOPE)
endfunction()

# the license files of the calling directory, for its targets: a dir of a library under 1stPartyLibs/ or 3rdPartyLibs/
# without any has those of the nearest dir above it within the library
function(_dagor_dir_licenses out)
  get_property(known DIRECTORY PROPERTY DAGOR_LICENSES SET)
  if(known)
    get_property(found DIRECTORY PROPERTY DAGOR_LICENSES)
    set(${out} "${found}" PARENT_SCOPE)
    return()
  endif()
  set(dir "${CMAKE_CURRENT_SOURCE_DIR}")
  _dagor_find_licenses("${dir}" found)
  while(NOT found AND dir MATCHES "/(1st|3rd)PartyLibs/[^/]+/" AND NOT EXISTS "${dir}/NO_LICENSE")
    cmake_path(GET dir PARENT_PATH dir)
    _dagor_find_licenses("${dir}" found)
  endwhile()
  if(NOT found AND dir MATCHES "/(1st|3rd)PartyLibs/" AND NOT EXISTS "${dir}/NO_LICENSE")
    message(FATAL_ERROR "${CMAKE_CURRENT_SOURCE_DIR} has no license file: add it, or a NO_LICENSE file if none is needed")
  endif()
  set_property(DIRECTORY PROPERTY DAGOR_LICENSES "${found}")
  set(${out} "${found}" PARENT_SCOPE)
endfunction()

function(dagor_target_licenses target)
  set(files)
  foreach(path IN LISTS ARGN)
    cmake_path(ABSOLUTE_PATH path NORMALIZE)
    if(IS_DIRECTORY "${path}")
      _dagor_find_licenses("${path}" found)
      list(APPEND files ${found})
    else()
      list(APPEND files "${path}")
    endif()
  endforeach()
  set_property(TARGET ${target} APPEND PROPERTY INTERFACE_DAGOR_LICENSE_FILES ${files})
endfunction()
