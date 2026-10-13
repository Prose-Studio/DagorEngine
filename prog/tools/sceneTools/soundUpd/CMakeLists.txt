set(deps
  engine.osApiWrappers
  engine.kernel
  engine.memory
  engine.ioSys
  engine.startup
  engine.baseUtil
  engine.math
  engine.perfMon.daProfilerStub
  gameLibs.gameResPatcher
  tools.libTools.util
)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME soundUpd EXECUTABLE LAX
  FILES_CMAKE soundUpd_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs
  BUILD_DEPENDENCIES PRIVATE ${deps}
  PROPERTIES DAGOR_EXCEPTIONS ON
  CDK
)
