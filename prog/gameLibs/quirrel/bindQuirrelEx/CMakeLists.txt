# The engine's Quirrel bindings (dagor.system, dagor.fs, time, shell, clipboard, localization, ...). On Linux the
# system functions of GUI programs (DAGOR_LINUX_GUI) differ from those of console ones; see dagor_add_link_choice().
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/3rdPartyLibs/pcre/pcre
  ${DAGOR_PROG_DIR}/3rdPartyLibs/utf8
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/libzip/lib
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
)
set(options)
if(WIN32)
  list(APPEND options /wd4548)
endif()
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  list(APPEND options -Wno-uninitialized)
endif()
set(deps engine.workCycle 3rdPartyLibs.pcre 3rdPartyLibs.uuidv7 3rdPartyLibs.arc.libzip gameLibs.iso8601Time)
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows)$" AND NOT DAGOR_ARCH STREQUAL "e2k")
  list(APPEND deps 3rdPartyLibs.cpu_features)
endif()
if(LINUX)
  foreach(build GUI noGUI)
    dagor_add_target(NAME gameLibs.quirrel.bindQuirrelEx.linux${build} STATIC
      FILES_CMAKE linux${build}_files.cmake
      INCLUDE_DIRECTORIES PRIVATE ${includes}
      COMPILE_DEFINITIONS PRIVATE ZIP_STATIC
      COMPILE_OPTIONS PRIVATE ${options}
      BUILD_DEPENDENCIES PRIVATE Dagor::QuirrelHeaders
    )
  endforeach()
  dagor_add_link_choice(gameLibs.quirrel.bindQuirrelEx.linuxSystem PROPERTY DAGOR_LINUX_GUI
    ON gameLibs.quirrel.bindQuirrelEx.linuxGUI OFF gameLibs.quirrel.bindQuirrelEx.linuxnoGUI)
  list(APPEND deps gameLibs.quirrel.bindQuirrelEx.linuxSystem)
endif()

dagor_add_target(NAME gameLibs.quirrel.bindQuirrelEx STATIC
  FILES_CMAKE bindQuirrelEx_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ZIP_STATIC
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel ${deps}
)
