set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/webui
  ${DAGOR_PROG_DIR}/dagorInclude
)
set(sources profilerPlugin.cpp)

dagor_add_library(gameLibs.webui.plugins.profiler ${sources})
target_include_directories(gameLibs.webui.plugins.profiler PRIVATE ${includes})
