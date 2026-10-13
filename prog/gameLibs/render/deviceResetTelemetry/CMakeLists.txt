dagor_add_target(NAME gameLibs.render.deviceResetTelemetry STATIC
  FILES_CMAKE deviceResetTelemetry_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.lib3d gameLibs.statsd
)
