set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/dagorInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
)
set(deps 3rdPartyLibs.image.libpng-1.4.22)
set(sources dargMcpPlugin.cpp)

dagor_add_library(gameLibs.webui.plugins.dargMcp ${sources})
target_include_directories(gameLibs.webui.plugins.dargMcp PRIVATE ${includes})
target_link_libraries(gameLibs.webui.plugins.dargMcp PRIVATE Dagor::Quirrel ${deps})
