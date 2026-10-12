set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/dagorInclude
)
set(sources sqDebuggerPlugin.cpp)
set(SourceStr quirrelDebugger.html)
list(APPEND stringify ${SourceStr})

dagor_add_library(gameLibs.webui.plugins.quirrel ${sources})
target_include_directories(gameLibs.webui.plugins.quirrel PRIVATE ${includes})
target_link_libraries(gameLibs.webui.plugins.quirrel PRIVATE Dagor::Quirrel)
dagor_target_stringify(gameLibs.webui.plugins.quirrel ${stringify})
