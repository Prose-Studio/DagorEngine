# Packages of games (CPack: cpack --preset, or the package workflow of a project's presets) and the apps of the mobile
# platforms.
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
#       the program as a macOS or iOS app bundle (MACOSX_BUNDLE) with the engine's Info.plist (templates/Info.plist.in,
#       Info-iOS.plist.in), signed ad hoc after each build
#   dagor_android_apk(<target> ID <package> ACTIVITY <class> [LABEL <label>] [VERSION <name>] [VERSION_CODE <n>]
#                     [ICON <png>] [ORIENTATION <screenOrientation>] [PERMISSIONS <permission>...]
#                     [JAVA <source>...] [ASSETS <path in the APK>|<file>...] [DEPENDS <target>...])
#       target <target>.apk: the APK of the app (an Android APPLICATION, the shared library of its NativeActivity), next
#       to the library, named like it: the manifest (templates/AndroidManifest.xml.in; ACTIVITY extends
#       android.app.NativeActivity), the Java sources of the app and of the libraries it links
#       (dagor_target_android_java) as classes.dex, the library and ASSETS, which the DEPENDS targets make. It is made
#       with the build tools of the Android SDK (DAGOR_ANDROID_SDK) and a JDK (scripts/android_apk.py says how it is
#       signed). Not in the default build.
#   dagor_target_android_java(<target> <source>...)
#       Java sources of a library's Android code (the classes its JNI calls use), in the APK of every app that links it
include_guard(GLOBAL)

if(ANDROID)
  set(DAGOR_ANDROID_TARGET_API 35 CACHE STRING "The target API level of Android apps")
  # the Android SDK: the NDK's (<sdk>/ndk/<version>), or ANDROID_HOME / ANDROID_SDK_ROOT
  set(_sdk)
  cmake_path(GET DAGOR_ANDROID_NDK PARENT_PATH _ndks)
  cmake_path(GET _ndks FILENAME _ndks_name)
  if(_ndks_name STREQUAL "ndk")
    cmake_path(GET _ndks PARENT_PATH _sdk)
  else()
    foreach(_var ANDROID_HOME ANDROID_SDK_ROOT)
      if(DEFINED ENV{${_var}} AND IS_DIRECTORY "$ENV{${_var}}")
        file(TO_CMAKE_PATH "$ENV{${_var}}" _sdk)
        break()
      endif()
    endforeach()
  endif()
  set(DAGOR_ANDROID_SDK "${_sdk}" CACHE PATH "The Android SDK (its build-tools and platforms make the APKs)")
  unset(_sdk)
  unset(_ndks)
  unset(_ndks_name)
endif()

function(dagor_apple_bundle target)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "NAME;ID;ICON;VERSION" "")
  if(arg_UNPARSED_ARGUMENTS OR NOT arg_NAME OR NOT arg_ID)
    message(FATAL_ERROR "dagor_apple_bundle(${target} NAME <name> ID <bundle id> ...)")
  endif()
  set(version "${arg_VERSION}")
  if(NOT version)
    set(version 1.0)
  endif()
  set(plist Info.plist.in)
  if(IOS)
    set(plist Info-iOS.plist.in)
  endif()
  set_target_properties(${target} PROPERTIES
    MACOSX_BUNDLE ON
    MACOSX_BUNDLE_INFO_PLIST "${DAGOR_CMAKE_DIR}/templates/${plist}"
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

function(dagor_target_android_java target)
  set(files)
  foreach(file IN LISTS ARGN)
    cmake_path(ABSOLUTE_PATH file NORMALIZE)
    list(APPEND files "${file}")
  endforeach()
  set_property(TARGET ${target} APPEND PROPERTY INTERFACE_DAGOR_ANDROID_JAVA ${files})
endfunction()

function(dagor_android_apk target)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "ID;ACTIVITY;LABEL;VERSION;VERSION_CODE;ICON;ORIENTATION"
    "PERMISSIONS;JAVA;ASSETS;DEPENDS")
  if(arg_UNPARSED_ARGUMENTS OR NOT arg_ID OR NOT arg_ACTIVITY)
    message(FATAL_ERROR "dagor_android_apk(${target} ID <package> ACTIVITY <class> ...)")
  endif()
  get_property(type TARGET ${target} PROPERTY TYPE)
  if(NOT ANDROID OR NOT type STREQUAL "SHARED_LIBRARY")
    message(FATAL_ERROR "dagor_android_apk(${target}): an Android APPLICATION (dagor_add_target) makes an APK")
  endif()
  # the tools: the SDK's newest build tools, the platform of the target API, a JDK (11 or later)
  file(GLOB build_tools LIST_DIRECTORIES true "${DAGOR_ANDROID_SDK}/build-tools/*")
  list(SORT build_tools COMPARE NATURAL ORDER DESCENDING)
  list(POP_FRONT build_tools build_tools)
  set(android_jar "${DAGOR_ANDROID_SDK}/platforms/android-${DAGOR_ANDROID_TARGET_API}/android.jar")
  if(NOT build_tools OR NOT EXISTS "${android_jar}")
    message(FATAL_ERROR "dagor_android_apk(${target}): the Android SDK (DAGOR_ANDROID_SDK='${DAGOR_ANDROID_SDK}') needs "
      "its build tools and platform: sdkmanager \"build-tools;<version>\" \"platforms;android-${DAGOR_ANDROID_TARGET_API}\"")
  endif()
  find_package(Java 11 REQUIRED COMPONENTS Development)
  file(REAL_PATH "${Java_JAVAC_EXECUTABLE}" javac)
  cmake_path(GET javac PARENT_PATH java_home)
  cmake_path(GET java_home PARENT_PATH java_home)

  # the manifest: the library's name in each configuration
  set(DAGOR_APK_ID "${arg_ID}")
  set(DAGOR_APK_ACTIVITY "${arg_ACTIVITY}")
  set(DAGOR_APK_LIB "$<TARGET_FILE_BASE_NAME:${target}>")
  set(DAGOR_APK_VERSION 1.0)
  if(arg_VERSION)
    set(DAGOR_APK_VERSION "${arg_VERSION}")
  endif()
  set(DAGOR_APK_VERSION_CODE 1)
  if(arg_VERSION_CODE)
    set(DAGOR_APK_VERSION_CODE "${arg_VERSION_CODE}")
  endif()
  set(DAGOR_APK_ORIENTATION sensorLandscape)
  if(arg_ORIENTATION)
    set(DAGOR_APK_ORIENTATION "${arg_ORIENTATION}")
  endif()
  set(DAGOR_APK_PERMISSIONS)
  foreach(permission IN LISTS arg_PERMISSIONS)
    string(APPEND DAGOR_APK_PERMISSIONS "  <uses-permission android:name=\"android.permission.${permission}\" />\n")
  endforeach()
  set(DAGOR_APK_ICON)
  set(icon)
  if(arg_ICON)
    set(DAGOR_APK_ICON "android:icon=\"@mipmap/icon\" ")
    cmake_path(ABSOLUTE_PATH arg_ICON NORMALIZE OUTPUT_VARIABLE icon)
  endif()
  set(gen "${CMAKE_CURRENT_BINARY_DIR}/gen/${target}/apk")
  configure_file("${DAGOR_CMAKE_DIR}/templates/AndroidManifest.xml.in" "${gen}/AndroidManifest.xml.in" @ONLY)
  file(GENERATE OUTPUT "${gen}/$<CONFIG>/AndroidManifest.xml" INPUT "${gen}/AndroidManifest.xml.in" TARGET ${target})

  # the APK's config: the Java sources of the app and of its link closure, the assets
  foreach(file IN LISTS arg_JAVA)
    cmake_path(ABSOLUTE_PATH file NORMALIZE)
    set_property(TARGET ${target} APPEND PROPERTY DAGOR_ANDROID_JAVA "${file}")
  endforeach()
  set(java "$<REMOVE_DUPLICATES:$<TARGET_PROPERTY:${target},DAGOR_ANDROID_JAVA>>")
  set(label "${arg_LABEL}")
  if(NOT label)
    set(label "${target}")
  endif()
  set(assets)
  foreach(asset IN LISTS arg_ASSETS)
    string(REPLACE "|" ";" parts "${asset}")
    list(GET parts 1 file)
    cmake_path(ABSOLUTE_PATH file NORMALIZE)
    list(GET parts 0 dest)
    string(APPEND assets "asset=${dest}|${file}\n")
  endforeach()
  set(apk "$<TARGET_FILE_DIR:${target}>/$<TARGET_FILE_BASE_NAME:${target}>.apk")
  string(CONCAT config
    "apk=${apk}\nwork=${gen}/$<CONFIG>/work\nmanifest=${gen}/$<CONFIG>/AndroidManifest.xml\nlabel=${label}\n"
    "lib=$<TARGET_FILE:${target}>\nstrip=${CMAKE_STRIP}\nabi=${ANDROID_ABI}\nmin_api=${DAGOR_ANDROID_API}\n"
    "android_jar=${android_jar}\nbuild_tools=${build_tools}\njava_home=${java_home}\n"
    "$<$<BOOL:${java}>:java=$<JOIN:${java},\njava=>\n>${assets}")
  if(icon)
    string(APPEND config "icon=${icon}\n")
  endif()
  file(GENERATE OUTPUT "${gen}/$<CONFIG>/apk.txt" CONTENT "${config}" TARGET ${target})
  # the script keeps track of what the APK is made of: it runs whenever the target is built
  add_custom_target(${target}.apk
    COMMAND "${Python3_EXECUTABLE}" "${DAGOR_CMAKE_DIR}/scripts/android_apk.py" "${gen}/$<CONFIG>/apk.txt"
    COMMENT "The APK of ${target}"
    VERBATIM)
  add_dependencies(${target}.apk ${target} ${arg_DEPENDS})
  set_property(TARGET ${target}.apk PROPERTY FOLDER "dagor")
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
