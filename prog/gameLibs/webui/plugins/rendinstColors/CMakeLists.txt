set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude)
set(sources rendinstColorsPlugin.cpp)
set(SourceHTML rendinstColors.html)
list(APPEND stringify ${SourceHTML})

dagor_add_library(gameLibs.webui.plugins.rendinstColors ${sources})
target_include_directories(gameLibs.webui.plugins.rendinstColors PRIVATE ${includes})
dagor_target_stringify(gameLibs.webui.plugins.rendinstColors ${stringify})
