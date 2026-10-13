# dsc2-nodeBased: compiles the node-based shaders of the web UI's shader editors (the compiler flavor of
# gameLibs/webui/plugins/shaderEditors) into the dumps games load
set(deps engine.osApiWrappers engine.kernel engine.memory.default.off engine.ioSys engine.startup engine.baseUtil
  engine.math engine.perfMon.daProfilerStub gameLibs.webui.plugins.shaderEditors.comp tools.libTools.util
  3rdPartyLibs.regExp)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME dsc2-nodeBased EXECUTABLE LAX
  FILES_CMAKE nodeBased_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)
