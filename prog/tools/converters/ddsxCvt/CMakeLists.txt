# ddsxCvt: converts DDS textures to the DDSx of a target platform through the DDSx plugins
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.perfMon.daProfilerStub tools.libTools.dtx tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME ddsxCvt EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE ddsxCvt_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)
