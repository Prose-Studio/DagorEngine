# binBlk: converts BLK files between text and binary form (the CDK's; jam built it rel only, so without a config
# suffix). The other utilities of this directory (jamfile, jamfile-misc) are not ported yet.
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.baseUtil engine.perfMon.daProfilerStub
  tools.libTools.util 3rdPartyLibs.openssl-3.x)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME binBlk EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE utils_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)
