# Packages of games (CPack): python project.py package, or cpack -C Rel in a game's tree.
#
#   dagor_package_game(<target> GAME_DIR <dir> [DATA <file or dir in the game dir>...] [NAME <launcher name>]
#                      [ARGS <argument>...])
#
# installs the game's program (the client, or the dedicated server in a tree with DAGOR_DEDICATED) into the component
# game or dedicated: the program, its LICENSE file and the runtime files of its libraries (SDK and driver DLLs) into
# <platform>-<arch>/ (the app bundle of dagor_apple_bundle() instead, signed ad hoc), the built DATA of GAME_DIR
# (shaders, vromfs, content: python project.py build makes them) and a launcher, NAME[-server].cmd / .sh, which runs
# the program from the package root as the game expects, with ARGS before the arguments it is given. The tree's
# package is a ZIP on Windows and a .tar.gz elsewhere named <project>[-dedicated]-<platform>-<arch>[-<version>]
# (the project's VERSION), of the configuration cpack is given (-C Rel).
include_guard(GLOBAL)

function(dagor_package_game target)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "GAME_DIR;NAME" "DATA;ARGS")
  if(arg_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "dagor_package_game(${target}): unexpected arguments: ${arg_UNPARSED_ARGUMENTS}")
  endif()
  if(NOT arg_GAME_DIR)
    message(FATAL_ERROR "dagor_package_game(${target}) needs GAME_DIR")
  endif()
  if(DAGOR_DAS_AOT_COMPILER)
    return() # the tree of the game's daScript AOT compiler
  endif()
  get_property(packaged GLOBAL PROPERTY DAGOR_PACKAGE_COMPONENT)
  if(packaged)
    message(FATAL_ERROR "dagor_package_game(${target}): the tree packages a game already")
  endif()
  _dagor_abs_paths(game_dir "${arg_GAME_DIR}")
  set(name "${arg_NAME}")
  if(NOT name)
    get_property(name GLOBAL PROPERTY DAGOR_GAME_CODENAME) # of dagor_add_dng_game
  endif()
  if(NOT name)
    set(name "${target}")
  endif()
  set(component game)
  if(DAGOR_DEDICATED)
    set(component dedicated)
    string(APPEND name "-server")
  endif()
  set(dest "${DAGOR_PLATFORM}-${DAGOR_ARCH}")
  get_property(bundle TARGET ${target} PROPERTY DAGOR_APPLE_BUNDLE) # dagor_apple_bundle()
  if(bundle)
    set(dest "${bundle}.app/Contents/MacOS")
  endif()

  # the program, its license and (at dagor_finalize) the runtime files of its libraries
  set(license_dir "$<TARGET_FILE_DIR:${target}>")
  set(license_dest "${dest}")
  if(bundle)
    string(APPEND license_dir "/../Resources") # see _dagor_licenses()
    set(license_dest "${bundle}.app/Contents/Resources")
  endif()
  install(PROGRAMS "$<TARGET_FILE:${target}>" DESTINATION "${dest}" COMPONENT ${component})
  install(FILES "${license_dir}/LICENSE-$<TARGET_FILE_BASE_NAME:${target}>" DESTINATION "${license_dest}"
    COMPONENT ${component})
  set_property(TARGET ${target} PROPERTY DAGOR_INSTALL_DIR "${dest}")
  set_property(TARGET ${target} PROPERTY DAGOR_INSTALL_COMPONENT ${component})
  if(bundle)
    # the rest of the bundle (signed at dagor_finalize, once its runtime files are in it too)
    get_property(bundle_files TARGET ${target} PROPERTY DAGOR_APPLE_BUNDLE_FILES)
    foreach(entry IN LISTS bundle_files)
      string(REPLACE "|" ";" parts "${entry}")
      list(GET parts 0 sub)
      list(GET parts 1 file)
      list(GET parts 2 file_name)
      install(FILES "${file}" DESTINATION "${bundle}.app/Contents/${sub}" RENAME "${file_name}" COMPONENT ${component})
    endforeach()
    set_property(GLOBAL PROPERTY DAGOR_PACKAGE_BUNDLE "${bundle}.app")
  endif()

  # the built data: a missing one stops the install (the package would not run)
  foreach(item IN LISTS arg_DATA)
    if(IS_ABSOLUTE "${item}" OR item MATCHES "(^|/)\\.\\.(/|$)")
      message(FATAL_ERROR "dagor_package_game(${target}): DATA ${item} is not in the game dir")
    endif()
    install(CODE "if(NOT EXISTS \"${game_dir}/${item}\")
  message(FATAL_ERROR \"${game_dir}/${item} is missing: build the game's data first (python project.py build)\")
endif()" COMPONENT ${component})
    cmake_path(GET item PARENT_PATH sub)
    if(item MATCHES "\\.[A-Za-z0-9]+$")
      install(FILES "${game_dir}/${item}" DESTINATION "./${sub}" COMPONENT ${component})
    else()
      install(DIRECTORY "${game_dir}/${item}" DESTINATION "./${sub}" COMPONENT ${component})
    endif()
  endforeach()

  # the launcher: the game finds its data in the working dir
  set(launcher_dir "${CMAKE_BINARY_DIR}/package")
  list(JOIN arg_ARGS " " args)
  if(args)
    string(APPEND args " ")
  endif()
  if(DAGOR_PLATFORM STREQUAL "windows")
    set(launcher "${name}.cmd")
    if(DAGOR_DEDICATED)
      set(run "\"%~dp0${dest}\\$<TARGET_FILE_NAME:${target}>\" ${args}%*") # in the console it is started from
    else()
      set(run "start \"\" \"%~dp0${dest}\\$<TARGET_FILE_NAME:${target}>\" ${args}%*")
    endif()
    set(text "@rem Runs ${name} from this dir, where its data is\n@pushd \"%~dp0\"\n@${run}\n@popd\n")
  else()
    set(launcher "${name}.sh")
    string(CONCAT text "#!/bin/sh\n# Runs ${name} from this dir, where its data is\ncd \"$(dirname \"$0\")\" || exit 1\n"
             "exec \"./${dest}/$<TARGET_FILE_NAME:${target}>\" ${args}\"$@\"\n")
  endif()
  set(newlines UNIX)
  if(DAGOR_PLATFORM STREQUAL "windows")
    set(newlines WIN32)
  endif()
  file(GENERATE OUTPUT "${launcher_dir}/$<CONFIG>/${launcher}" CONTENT "${text}" NEWLINE_STYLE ${newlines})
  install(PROGRAMS "${launcher_dir}/$<CONFIG>/${launcher}" DESTINATION . COMPONENT ${component})

  set_property(GLOBAL PROPERTY DAGOR_PACKAGE_COMPONENT ${component})
endfunction()

# dagor_apple_bundle(<target> NAME <name> ID <bundle id> DIR <dir> [ICON <.icns>] [VERSION <version>]
#                    [PLIST <Info.plist template>]): the program as the app bundle <DIR>/<NAME>.app (macOS):
#   Contents/MacOS/<program> (the names of the configurations differ by their postfix), Contents/Info.plist from the
#   template (prog/cmake/templates/Info.plist.in: @BUNDLE_EXECUTABLE@, @BUNDLE_NAME@, @BUNDLE_ID@, @BUNDLE_ICON@,
#   @BUNDLE_VERSION@, @BUNDLE_MIN_SYSTEM@), naming the program of the configuration built last, and
#   Contents/Resources/<NAME>.icns; signed ad hoc after each build. Called in the directory that declares <target>;
#   dagor_package_game() packages the bundle.
function(dagor_apple_bundle target)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "NAME;ID;DIR;ICON;VERSION;PLIST" "")
  if(arg_UNPARSED_ARGUMENTS OR NOT arg_NAME OR NOT arg_ID OR NOT arg_DIR)
    message(FATAL_ERROR "dagor_apple_bundle(${target} NAME <name> ID <bundle id> DIR <dir> ...)")
  endif()
  if(NOT DAGOR_PLATFORM STREQUAL "macOS")
    message(FATAL_ERROR "dagor_apple_bundle(${target}): app bundles are for macOS")
  endif()
  _dagor_abs_paths(dir "${arg_DIR}")
  set(contents "${dir}/${arg_NAME}.app/Contents")
  set_target_properties(${target} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "$<1:${contents}/MacOS>"
    DAGOR_APPLE_BUNDLE "${arg_NAME}")

  set(plist "${arg_PLIST}")
  if(plist)
    _dagor_abs_paths(plist "${plist}")
  else()
    set(plist "${DAGOR_CMAKE_DIR}/templates/Info.plist.in")
  endif()
  set(BUNDLE_EXECUTABLE "$<TARGET_FILE_NAME:${target}>")
  set(BUNDLE_NAME "${arg_NAME}")
  set(BUNDLE_ID "${arg_ID}")
  set(BUNDLE_ICON "")
  if(arg_ICON)
    set(BUNDLE_ICON "${arg_NAME}")
  endif()
  set(BUNDLE_VERSION "${arg_VERSION}")
  if(NOT BUNDLE_VERSION)
    set(BUNDLE_VERSION "1.0")
  endif()
  set(BUNDLE_MIN_SYSTEM "${CMAKE_OSX_DEPLOYMENT_TARGET}")
  set(gen "${CMAKE_CURRENT_BINARY_DIR}/gen/${target}/bundle")
  configure_file("${plist}" "${gen}/Info.plist.in" @ONLY)
  file(GENERATE OUTPUT "${gen}/$<CONFIG>/Info.plist" INPUT "${gen}/Info.plist.in")

  set(files "|${gen}/$<CONFIG>/Info.plist|Info.plist")
  set(commands COMMAND "${CMAKE_COMMAND}" -E copy_if_different "${gen}/$<CONFIG>/Info.plist" "${contents}/Info.plist")
  if(arg_ICON)
    _dagor_abs_paths(icon "${arg_ICON}")
    list(APPEND files "Resources|${icon}|${arg_NAME}.icns")
    list(APPEND commands COMMAND "${CMAKE_COMMAND}" -E make_directory "${contents}/Resources"
                         COMMAND "${CMAKE_COMMAND}" -E copy_if_different "${icon}" "${contents}/Resources/${arg_NAME}.icns")
  endif()
  set_property(TARGET ${target} PROPERTY DAGOR_APPLE_BUNDLE_FILES "${files}")
  add_custom_command(TARGET ${target} POST_BUILD ${commands}
    COMMAND codesign --force --sign - "${dir}/${arg_NAME}.app"
    COMMENT "App bundle ${arg_NAME}.app"
    VERBATIM)
endfunction()

# called by dagor_finalize(): CPack for the tree's game package
function(_dagor_package)
  get_property(component GLOBAL PROPERTY DAGOR_PACKAGE_COMPONENT)
  if(NOT component)
    return()
  endif()
  get_property(bundle GLOBAL PROPERTY DAGOR_PACKAGE_BUNDLE)
  if(bundle)
    # the installed bundle signed as a whole (ad hoc: it runs on the machines that allow that)
    install(CODE "execute_process(COMMAND codesign --force --sign - \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/${bundle}\"
  COMMAND_ERROR_IS_FATAL ANY)" COMPONENT ${component})
  endif()
  set(name "${PROJECT_NAME}")
  if(component STREQUAL "dedicated")
    string(APPEND name "-dedicated")
  endif()
  string(APPEND name "-${DAGOR_PLATFORM}-${DAGOR_ARCH}")
  if(PROJECT_VERSION)
    string(APPEND name "-${PROJECT_VERSION}")
  endif()
  set(CPACK_PACKAGE_NAME "${PROJECT_NAME}")
  set(CPACK_PACKAGE_FILE_NAME "${name}")
  if(PROJECT_VERSION)
    set(CPACK_PACKAGE_VERSION "${PROJECT_VERSION}")
  endif()
  if(DAGOR_PLATFORM STREQUAL "windows")
    set(CPACK_GENERATOR ZIP)
  else()
    set(CPACK_GENERATOR TGZ)
  endif()
  set(CPACK_COMPONENTS_ALL ${component})
  set(CPACK_ARCHIVE_COMPONENT_INSTALL ON)
  set(CPACK_COMPONENTS_GROUPING ALL_COMPONENTS_IN_ONE) # one archive, without a component suffix
  set(CPACK_COMPONENT_INCLUDE_TOPLEVEL_DIRECTORY ON) # it extracts into a dir of its name
  set(CPACK_PACKAGE_DIRECTORY "${CMAKE_SOURCE_DIR}/../build/packages")
  include(CPack)
endfunction()
