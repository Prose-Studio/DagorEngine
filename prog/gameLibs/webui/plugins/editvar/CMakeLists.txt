set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude)
set(sources editVarPlugin.cpp)
set(SourceStr editVar.html)
list(APPEND stringify ${SourceStr})

dagor_add_library(gameLibs.webui.plugins.editvar ${sources})
target_include_directories(gameLibs.webui.plugins.editvar PRIVATE ${includes})
dagor_target_stringify(gameLibs.webui.plugins.editvar ${stringify})
