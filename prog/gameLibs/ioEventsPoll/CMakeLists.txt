set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/libev)
if(WIN32)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/posix/include/win32)
endif()
if(APPLE)
  set(options -Wno-c++1z-compat-mangling)
endif()

dagor_add_target(NAME gameLibs.ioEventsPoll STATIC LAX
  FILES_CMAKE ioEventsPoll_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.libev
)
