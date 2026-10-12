# The engine's tools that build steps run (the CDK: shader compilers, vromfsPacker, daBuild, the parser generators).
#
#   dagor_host_tool(<tool> <out-var>)
#
# sets <out-var> to the program to run and <out-var>_DEPENDS to what a custom command running it depends on:
#   - DAGOR_HOST_TOOLS_DIR (a CDK, e.g. tools/dagor_cdk/windows-x86_64 of a prebuilt engine): the program there;
#   - an engine tree that is not cross-compiling: the tree's own target;
#   - otherwise (games, cross builds) the engine's CDK for the host, built on demand: target dagor.hostTools.<variant>
#     configures and builds the engine's <host>-cdk preset (the editor tools, daBuild and its plugins: <host>-editor), the trees
#     cmake --preset makes in <engine>/build, and installs them into <engine>/tools/dagor_cdk/<host>. Trees sharing it
#     build it under a lock, one at a time; when it is up to date that is a quick check.
#
#   dagor_install_cdk(<target> [SUBDIR <dir>])
#
# installs a tool of the CDK (component cdk) into tools/dagor_cdk/<platform>-<arch>[/<dir>] of the install prefix (the
# engine root in the engine's presets) with its runtime files, its LICENSE file and its debug info.
include_guard(GLOBAL)

set(DAGOR_HOST_TOOLS_DIR "" CACHE PATH "A CDK (prebuilt engine tools) for the build steps; empty builds the engine's")

# the CDK tools of the editor tree (on the shared kernel; daBuild loads the exporter plugins built with it)
set(_DAGOR_EDITOR_HOST_TOOLS daBuild ddsxCvt2)
# the CDK tools jam built rel only, without a config postfix (dagor_install_cdk checks this list)
set(DAGOR_CDK_NO_POSTFIX binBlk ddsx2dds ddsxCvt dolphin whale duktape pcDdsxConv iosDdsxConv andDdsxConv)

function(dagor_host_tool tool out)
  set(file "${tool}-dev")
  if(tool IN_LIST DAGOR_CDK_NO_POSTFIX)
    set(file "${tool}")
  endif()
  string(APPEND file "${CMAKE_HOST_EXECUTABLE_SUFFIX}")
  if(DAGOR_HOST_TOOLS_DIR)
    if(NOT EXISTS "${DAGOR_HOST_TOOLS_DIR}/${file}")
      message(FATAL_ERROR "DAGOR_HOST_TOOLS_DIR='${DAGOR_HOST_TOOLS_DIR}' has no ${file}")
    endif()
    set(${out} "${DAGOR_HOST_TOOLS_DIR}/${file}" PARENT_SCOPE)
    set(${out}_DEPENDS "${DAGOR_HOST_TOOLS_DIR}/${file}" PARENT_SCOPE)
    return()
  endif()
  if(NOT DAGOR_VARIANT STREQUAL "game" AND NOT CMAKE_CROSSCOMPILING)
    set(${out} "$<TARGET_FILE:${tool}>" PARENT_SCOPE)
    set(${out}_DEPENDS ${tool} PARENT_SCOPE)
    return()
  endif()

  set(variant cdk)
  if(tool IN_LIST _DAGOR_EDITOR_HOST_TOOLS)
    set(variant editor)
  endif()
  if(NOT TARGET dagor.hostTools.${variant})
    string(TOLOWER "${DAGOR_HOST_PLATFORM}" host)
    add_custom_target(dagor.hostTools.${variant}
      COMMAND "${CMAKE_COMMAND}" -E env DAGOR_DEPS_DIR=${DAGOR_DEPS_DIR}
        "${CMAKE_COMMAND}" -DSOURCE_DIR=${DAGOR_PROG_DIR} -DPRESET=${host}-${variant} -DCOMPONENT=cdk
        -P "${DAGOR_CMAKE_DIR}/scripts/build_preset.cmake"
      COMMENT "The engine's host tools (${host}-${variant})"
      USES_TERMINAL
      VERBATIM)
    set_property(TARGET dagor.hostTools.${variant} PROPERTY FOLDER "dagor")
  endif()
  set(${out} "${DAGOR_ENGINE_ROOT}/tools/dagor_cdk/${DAGOR_HOST_TAG}/${file}" PARENT_SCOPE)
  set(${out}_DEPENDS dagor.hostTools.${variant} PARENT_SCOPE)
endfunction()

function(dagor_install_cdk target)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "SUBDIR" "")
  get_property(postfix TARGET ${target} PROPERTY DEV_POSTFIX)
  if(target IN_LIST DAGOR_CDK_NO_POSTFIX AND postfix)
    message(FATAL_ERROR "CDK tool ${target} has a config postfix: drop it from DAGOR_CDK_NO_POSTFIX (DagorHostTools.cmake)")
  elseif(NOT target IN_LIST DAGOR_CDK_NO_POSTFIX AND NOT postfix)
    message(FATAL_ERROR "CDK tool ${target} has no config postfix: add it to DAGOR_CDK_NO_POSTFIX (DagorHostTools.cmake)")
  endif()
  set(dest "tools/dagor_cdk/${DAGOR_PLATFORM}-${DAGOR_ARCH}")
  if(arg_SUBDIR)
    string(APPEND dest "/${arg_SUBDIR}")
  endif()
  dagor_install_program(${target} DESTINATION "${dest}" COMPONENT cdk)
endfunction()
