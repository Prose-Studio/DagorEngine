# The engine's binding of Breakpad: installs the crash handler and writes minidumps for the crash reporter
if(NOT CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux|Windows)$")
  message(FATAL_ERROR "gameLibs/breakpad/binder does not support ${DAGOR_PLATFORM}: use gameLibs/breakpad/binder/stub")
endif()
set(includes
  ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/minhook/include
)
set(deps 1stPartyLibs.sysinfo 3rdPartyLibs.breakpad 3rdPartyLibs.eastl engine.osApiWrappers engine.startup
  gameLibs.folders)
set(sources callbacks.cpp binder.cpp)
if(WIN32 AND NOT DAGOR_ARCH STREQUAL "arm64")
  list(APPEND deps 3rdPartyLibs.minhook)
endif()

dagor_add_library(gameLibs.breakpad.binder ${sources})
target_include_directories(gameLibs.breakpad.binder PRIVATE ${includes})
target_link_libraries(gameLibs.breakpad.binder PRIVATE ${deps})
