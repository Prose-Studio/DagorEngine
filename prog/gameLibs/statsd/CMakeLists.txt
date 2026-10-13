dagor_add_target(NAME gameLibs.statsd STATIC
  FILES_CMAKE statsd_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.asyncResolveAddr
)
