# vromfsPacker: the virtual ROM file system (vromfs) pack builder (gameLibs/vromfsPacker)
set(deps engine.kernel engine.memory engine.perfMon.daProfilerStub engine.startup engine.math gameLibs.vromfsPacker)
if(WIN32)
  list(APPEND libs System::advapi32)
endif()
if(LINUX)
  set(libs System::dl)
endif()
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME vromfsPacker EXECUTABLE LAX
  FILES_CMAKE vromfsPacker_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
  PROPERTIES DAGOR_EXCEPTIONS ON
  CDK
)
