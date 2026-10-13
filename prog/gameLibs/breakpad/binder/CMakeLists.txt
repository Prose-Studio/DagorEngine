# The engine's binding of Breakpad (Windows, Linux, macOS): installs the crash handler and writes minidumps for the crash
# reporter
set(deps 1stPartyLibs.sysinfo 3rdPartyLibs.breakpad 3rdPartyLibs.eastl engine.osApiWrappers engine.startup
  gameLibs.folders)
if(WIN32 AND NOT DAGOR_ARCH STREQUAL "arm64")
  list(APPEND deps 3rdPartyLibs.minhook)
endif()

dagor_add_target(NAME gameLibs.breakpad.binder STATIC
  FILES_CMAKE binder_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/minhook/include
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
