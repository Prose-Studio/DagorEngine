set(FILES callbacks.c compress.c enet_dagor.c host.c list.c packet.c peer.c protocol.c)
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|iOS|tvOS)$")
  list(APPEND FILES unix.c)
endif()
