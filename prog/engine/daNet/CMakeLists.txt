# daNet: the ENet based network transport
add_subdirectory(delta)
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng ${DAGOR_PROG_DIR}/3rdPartyLibs/enet/include)
set(deps 3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.enet)
if(WIN32)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/posix/include/win32)
  list(APPEND deps 3rdPartyLibs.posix)
endif()

dagor_add_target(NAME engine.daNet STATIC
  FILES_CMAKE daNet_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
