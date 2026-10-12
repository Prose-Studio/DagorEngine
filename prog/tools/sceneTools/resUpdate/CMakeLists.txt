# resUpd: updates game resource packs, vromfs packs and sound banks from new vromfs (gameResPatcher)
set(includes ${DAGOR_PROG_DIR}/gameLibs ${DAGOR_PROG_DIR}/tools/sharedInclude)
set(sources resUpdate.cpp cmain.cpp)
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.perfMon.daProfilerStub gameLibs.gameResPatcher tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_executable(resUpd LAX ${sources})
target_include_directories(resUpd PRIVATE ${includes})
target_link_libraries(resUpd PRIVATE ${deps})
set_target_properties(resUpd PROPERTIES DAGOR_EXCEPTIONS ON)
dagor_install_cdk(resUpd)
