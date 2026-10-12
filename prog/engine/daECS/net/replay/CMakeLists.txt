if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps engine.ioSys)
endif()

dagor_add_target(NAME engine.daECS.net.replay STATIC
  FILES_CMAKE replay_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
