# Packages of games (CPack: cpack --preset, or the package workflow of a project's presets).
#
#   dagor_package_game(<target> GAME_DIR <dir> [DATA <file or dir in the game dir>...] [NAME <launcher name>]
#                      [ARGS <argument>...])
#       installs the game's program (the client, or the dedicated server in a tree with DAGOR_DEDICATED) into component
#       game or dedicated: the program (or its app bundle) with its runtime files and LICENSE into <platform>-<arch>/,
#       the built DATA of GAME_DIR (shaders, vromfs, content) and a launcher, NAME[-server].cmd / .sh, which runs the
#       program from the package root as the game expects, with ARGS before the arguments it is given. The package is a
#       ZIP on Windows and a .tar.gz elsewhere, <project>[-dedicated]-<platform>-<arch>[-<version>], in
#       <build>/packages.
#   dagor_apple_bundle(<target> NAME <name> ID <bundle id> [ICON <.icns>] [VERSION <version>])
#       the program as a macOS app bundle (MACOSX_BUNDLE) with the engine's Info.plist (templates/Info.plist.in), signed
#       ad hoc after each build
include_guard(GLOBAL)

function(dagor_apple_bundle target)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "NAME;ID;ICON;VERSION" "")
  if(arg_UNPARSED_ARGUMENTS OR NOT arg_NAME OR NOT arg_ID)
    message(FATAL_ERROR "dagor_apple_bundle(${target} NAME <name> ID <bundle id> ...)")
  endif()
  set(version "${arg_VERSION}")
  if(NOT version)
    set(version 1.0)
  endif()
  set_target_properties(${target} PROPERTIES
    MACOSX_BUNDLE ON
    MACOSX_BUNDLE_INFO_PLIST "${DAGOR_CMAKE_DIR}/templates/Info.plist.in"
    MACOSX_BUNDLE_BUNDLE_NAME "${arg_NAME}"
    MACOSX_BUNDLE_GUI_IDENTIFIER "${arg_ID}"
    MACOSX_BUNDLE_SHORT_VERSION_STRING "${version}"
    MACOSX_BUNDLE_BUNDLE_VERSION "${version}")
  if(arg_ICON)
    cmake_path(ABSOLUTE_PATH arg_ICON NORMALIZE OUTPUT_VARIABLE icon)
    cmake_path(GET icon FILENAME icon_name)
    target_sources(${target} PRIVATE "${icon}")
    set_source_files_properties("${icon}" PROPERTIES MACOSX_PACKAGE_LOCATION Resources)
    set_property(TARGET ${target} PROPERTY MACOSX_BUNDLE_ICON_FILE "${icon_name}")
  endif()
  add_custom_command(TARGET ${target} POST_BUILD
    COMMAND codesign --force --sign - "$<TARGET_BUNDLE_DIR:${target}>"
    VERBATIM)
endfunction()

function(dagor_package_game target)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "GAME_DIR;NAME" "DATA;ARGS")
  if(arg_UNPARSED_ARGUMENTS OR NOT arg_GAME_DIR)
    message(FATAL_ERROR "dagor_package_game(${target} GAME_DIR <dir> ...)")
  endif()
  if(DAGOR_DAS_AOT_COMPILER)
    return() # the tree of the game's daScript AOT compiler
  endif()
  cmake_path(ABSOLUTE_PATH arg_GAME_DIR NORMALIZE OUTPUT_VARIABLE game_dir)
  set(name "${arg_NAME}")
  if(NOT name)
    get_property(name GLOBAL PROPERTY DAGOR_GAME_CODENAME)
  endif()
  set(component game)
  if(DAGOR_DEDICATED)
    set(component dedicated)
    string(APPEND name "-server")
  endif()
  set(dest "${DAGOR_PLATFORM}-${DAGOR_ARCH}")
  dagor_install_program(${target} DESTINATION "${dest}" COMPONENT ${component})
  get_property(bundle TARGET ${target} PROPERTY MACOSX_BUNDLE)
  if(bundle)
    install(CODE "execute_process(COMMAND codesign --force --sign -
  \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/${dest}/$<TARGET_FILE_NAME:${target}>.app\" COMMAND_ERROR_IS_FATAL ANY)"
      COMPONENT ${component})
    set(program "${dest}/$<TARGET_FILE_NAME:${target}>.app/Contents/MacOS/$<TARGET_FILE_NAME:${target}>")
  else()
    set(program "${dest}/$<TARGET_FILE_NAME:${target}>")
  endif()

  # the built data: a missing one stops the install (the package would not run)
  foreach(item IN LISTS arg_DATA)
    if(IS_ABSOLUTE "${item}" OR item MATCHES "(^|/)\\.\\.(/|$)")
      message(FATAL_ERROR "dagor_package_game(${target}): DATA ${item} is not in the game dir")
    endif()
    install(CODE "if(NOT EXISTS \"${game_dir}/${item}\")
  message(FATAL_ERROR \"${game_dir}/${item} is missing: build the game's content first\")
endif()" COMPONENT ${component})
    cmake_path(GET item PARENT_PATH sub)
    if(IS_DIRECTORY "${game_dir}/${item}" OR NOT item MATCHES "\\.[A-Za-z0-9]+$")
      install(DIRECTORY "${game_dir}/${item}" DESTINATION "./${sub}" COMPONENT ${component})
    else()
      install(FILES "${game_dir}/${item}" DESTINATION "./${sub}" COMPONENT ${component})
    endif()
  endforeach()

  # the launcher: the game finds its data in the working dir
  list(JOIN arg_ARGS " " args)
  if(args)
    string(APPEND args " ")
  endif()
  if(WIN32)
    set(launcher "${name}.cmd")
    string(REPLACE "/" "\\" program "${program}")
    set(run "\"%~dp0${program}\" ${args}%*") # the server in the console it is started from
    if(NOT DAGOR_DEDICATED)
      set(run "start \"\" ${run}")
    endif()
    set(text "@rem Runs ${name} from this dir, where its data is\n@pushd \"%~dp0\"\n@${run}\n@popd\n")
    set(newlines WIN32)
  else()
    set(launcher "${name}.sh")
    string(CONCAT text "#!/bin/sh\n# Runs ${name} from this dir, where its data is\ncd \"$(dirname \"$0\")\" || exit 1\n"
             "exec \"./${program}\" ${args}\"$@\"\n")
    set(newlines UNIX)
  endif()
  file(GENERATE OUTPUT "${CMAKE_BINARY_DIR}/package/$<CONFIG>/${launcher}" CONTENT "${text}" NEWLINE_STYLE ${newlines})
  install(PROGRAMS "${CMAKE_BINARY_DIR}/package/$<CONFIG>/${launcher}" DESTINATION . COMPONENT ${component})

  set(package "${PROJECT_NAME}")
  if(DAGOR_DEDICATED)
    string(APPEND package "-dedicated")
  endif()
  string(APPEND package "-${DAGOR_PLATFORM}-${DAGOR_ARCH}")
  if(PROJECT_VERSION)
    string(APPEND package "-${PROJECT_VERSION}")
    set(CPACK_PACKAGE_VERSION "${PROJECT_VERSION}")
  endif()
  set(CPACK_PACKAGE_NAME "${PROJECT_NAME}")
  set(CPACK_PACKAGE_FILE_NAME "${package}")
  set(CPACK_GENERATOR TGZ)
  if(WIN32)
    set(CPACK_GENERATOR ZIP)
  endif()
  set(CPACK_COMPONENTS_ALL ${component})
  set(CPACK_ARCHIVE_COMPONENT_INSTALL ON)
  set(CPACK_COMPONENTS_GROUPING ALL_COMPONENTS_IN_ONE) # one archive, without a component suffix
  set(CPACK_COMPONENT_INCLUDE_TOPLEVEL_DIRECTORY ON) # it extracts into a dir of its name
  set(CPACK_PACKAGE_DIRECTORY "${CMAKE_BINARY_DIR}/packages")
  include(CPack)
endfunction()
