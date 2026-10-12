set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/webui
  ${DAGOR_PROG_DIR}/dagorInclude
)
set(sources shaderPlugin.cpp)
list(APPEND stringify shaderVars.html)

dagor_add_library(gameLibs.webui.plugins.shadervars ${sources})
target_include_directories(gameLibs.webui.plugins.shadervars PRIVATE ${includes})
dagor_target_stringify(gameLibs.webui.plugins.shadervars ${stringify})
