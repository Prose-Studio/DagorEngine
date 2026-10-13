# resDiffUtil: builds patches of game resource packs (GRP/DxP) between a base and a new game root
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.perfMon.daProfilerStub tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME resDiffUtil EXECUTABLE LAX
  FILES_CMAKE resDiff_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)
