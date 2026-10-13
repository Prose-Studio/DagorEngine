set(deps
  engine.osApiWrappers
  engine.kernel
  engine.memory
  engine.ioSys
  engine.startup
  engine.baseUtil
  engine.math
  engine.coreUtil
  engine.perfMon.daProfilerStub
  tools.libTools.util
)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME wsos EXECUTABLE LAX
  FILES_CMAKE wsos_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)
