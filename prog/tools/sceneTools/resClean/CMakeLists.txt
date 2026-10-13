# resCleanUtil: finds (and with -clean removes) GRP/DxP files not in the resource pack list of a vromfs
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.perfMon.daProfilerStub tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME resCleanUtil EXECUTABLE LAX
  FILES_CMAKE resClean_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)
