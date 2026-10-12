# The web UI's websocket stream without a server (platforms without mongoose)
dagor_add_library(gameLibs.webui.websocket.stub webSocketStream.cpp)
target_include_directories(gameLibs.webui.websocket.stub PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
