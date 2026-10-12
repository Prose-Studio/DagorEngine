dagor_add_target(NAME gameLibs.render.deviceResetTelemetry STATIC
  FILES_CMAKE deviceResetTelemetry_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude
  BUILD_DEPENDENCIES PRIVATE engine.lib3d gameLibs.statsd
)
