# dsc2-nodeBased: compiles the node-based shaders of the web UI's shader editors (the compiler flavor of
# gameLibs/webui/plugins/shaderEditors) into the dumps games load
set(deps engine.osApiWrappers engine.kernel engine.memory.default.off engine.ioSys engine.startup engine.baseUtil
  engine.math engine.perfMon.daProfilerStub gameLibs.webui.plugins.shaderEditors.comp tools.libTools.util
  3rdPartyLibs.regExp)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_executable(dsc2-nodeBased LAX main.cpp winmain_con.cpp)
target_include_directories(dsc2-nodeBased PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/tools/sharedInclude)
target_link_libraries(dsc2-nodeBased PRIVATE ${deps})
dagor_install_cdk(dsc2-nodeBased)
