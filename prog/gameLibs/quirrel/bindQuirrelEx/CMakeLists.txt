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
set(sources
  sqRegExp.cpp
  sqUtf8.cpp
  autoBind.cpp
  autoCleanup.cpp
  bindSqrat.cpp
  sqModulesDagor.cpp
  fileDropHandler.cpp
  screenshotMetaInfoLoader.cpp
  sqratDagorMath.cpp
  sqratDagorDebug.cpp
  logerrSqInterceptor.cpp
  sqratDataBlock.cpp
  sqratIso8601Time.cpp
  random.cpp
  hash.cpp
  zipArchive.cpp
  platformMisc.cpp
  cpuinfo.cpp
  dagorSystem.cpp
  dagorSystemFileHandlers.cpp
  dagorTime.cpp
  dagorWorkCycle.cpp
  dagorFS.cpp
  dagorFolders.cpp
  dagorShell.cpp
  dagorClipboard.cpp
  localization.cpp
  chinese-hypenation.cpp
  japanese-hypenation.cpp
  helpers.cpp
)
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND sources dagorSystemMac.mm)
endif()
if(WIN32)
  list(APPEND options /wd4548)
endif()
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  list(APPEND options -Wno-uninitialized)
endif()
list(APPEND defines ZIP_STATIC)
set(deps engine.workCycle 3rdPartyLibs.pcre 3rdPartyLibs.uuidv7 3rdPartyLibs.arc.libzip gameLibs.iso8601Time)
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows)$" AND NOT DAGOR_ARCH STREQUAL "e2k")
  list(APPEND deps 3rdPartyLibs.cpu_features)
endif()
if(LINUX)
  foreach(build GUI noGUI)
    set(file dagorSystemLinux.cpp)
    if(build STREQUAL "noGUI")
      set(file dagorSystemLinuxStub.cpp)
    endif()
    dagor_add_library(gameLibs.quirrel.bindQuirrelEx.linux${build} ${file})
    target_include_directories(gameLibs.quirrel.bindQuirrelEx.linux${build} PRIVATE ${includes})
    target_compile_definitions(gameLibs.quirrel.bindQuirrelEx.linux${build} PRIVATE ${defines})
    target_compile_options(gameLibs.quirrel.bindQuirrelEx.linux${build} PRIVATE ${options})
    target_link_libraries(gameLibs.quirrel.bindQuirrelEx.linux${build} PRIVATE Dagor::QuirrelHeaders)
  endforeach()
  dagor_add_link_choice(gameLibs.quirrel.bindQuirrelEx.linuxSystem PROPERTY DAGOR_LINUX_GUI
    ON gameLibs.quirrel.bindQuirrelEx.linuxGUI OFF gameLibs.quirrel.bindQuirrelEx.linuxnoGUI)
  list(APPEND deps gameLibs.quirrel.bindQuirrelEx.linuxSystem)
endif()

dagor_add_library(gameLibs.quirrel.bindQuirrelEx ${sources})
target_include_directories(gameLibs.quirrel.bindQuirrelEx PRIVATE ${includes})
target_compile_definitions(gameLibs.quirrel.bindQuirrelEx PRIVATE ${defines})
target_compile_options(gameLibs.quirrel.bindQuirrelEx PRIVATE ${options})
target_link_libraries(gameLibs.quirrel.bindQuirrelEx PRIVATE Dagor::Quirrel ${deps})
