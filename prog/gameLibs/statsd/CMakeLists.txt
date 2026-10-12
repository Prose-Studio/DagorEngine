dagor_add_target(NAME gameLibs.statsd STATIC
  FILES_CMAKE statsd_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE gameLibs.asyncResolveAddr
)
