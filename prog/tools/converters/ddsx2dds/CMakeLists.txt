# ddsx2dds: converts DDSx textures back to DDS (PC formats) and dumps their headers
dagor_add_target(NAME ddsx2dds EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE ddsx2dds_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.osApiWrappers.messageBox.stub engine.kernel engine.memory engine.ioSys engine.startup
    engine.baseUtil engine.math engine.perfMon.daProfilerStub
  CDK
)
