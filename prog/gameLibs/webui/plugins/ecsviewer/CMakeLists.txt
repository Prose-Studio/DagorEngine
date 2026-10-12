set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs
  ${DAGOR_PROG_DIR}/dagorInclude
)
set(sources ecsViewerPlugin.cpp ecsViewerPluginListener.cpp)
set(SourceHTML ecsViewer.html)
list(APPEND stringify ${SourceHTML})

dagor_add_library(gameLibs.webui.plugins.ecsviewer ${sources})
target_include_directories(gameLibs.webui.plugins.ecsviewer PRIVATE ${includes})
dagor_target_stringify(gameLibs.webui.plugins.ecsviewer ${stringify})
