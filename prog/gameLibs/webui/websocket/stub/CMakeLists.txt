# The web UI's websocket stream without a server (platforms without mongoose)
dagor_add_library(STRICT SOURCES webSocketStream.cpp PRIVATE_INCLUDES ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
