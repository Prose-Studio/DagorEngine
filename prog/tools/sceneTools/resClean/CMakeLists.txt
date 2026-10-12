# resCleanUtil: finds (and with -clean removes) GRP/DxP files not in the resource pack list of a vromfs
set(sources resCleanUtil.cpp)
set(includes ${DAGOR_PROG_DIR}/engine ${DAGOR_PROG_DIR}/tools/sharedInclude)
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.perfMon.daProfilerStub tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_executable(resCleanUtil LAX ${sources})
target_include_directories(resCleanUtil PRIVATE ${includes})
target_link_libraries(resCleanUtil PRIVATE ${deps})
dagor_install_cdk(resCleanUtil)
