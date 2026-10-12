add_subdirectory(stub)

set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/dagorInclude
  ${DAGOR_PROG_DIR}/engine/sharedInclude
)
set(sources webSocketStream.cpp)
set(deps 3rdPartyLibs.mongoose)

dagor_add_library(gameLibs.webui.websocket ${sources})
target_include_directories(gameLibs.webui.websocket PRIVATE ${includes})
target_link_libraries(gameLibs.webui.websocket PRIVATE ${deps})
