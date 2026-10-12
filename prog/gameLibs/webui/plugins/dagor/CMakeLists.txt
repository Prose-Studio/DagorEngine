set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/webui
  ${DAGOR_PROG_DIR}/dagorInclude
)
set(sources dagorplugins.cpp)
list(APPEND stringify_array showMemFlameGraph.html)
if(DAGOR_BUILDING_TOOLS)
  list(APPEND defines _TARGET_PC_TOOLS_BUILD)
else()
  list(APPEND sources memmap.cpp)
endif()

dagor_add_library(gameLibs.webui.plugins.dagor ${sources})
target_include_directories(gameLibs.webui.plugins.dagor PRIVATE ${includes})
target_compile_definitions(gameLibs.webui.plugins.dagor PRIVATE ${defines})
dagor_target_stringify(gameLibs.webui.plugins.dagor ARRAY ${stringify_array})
