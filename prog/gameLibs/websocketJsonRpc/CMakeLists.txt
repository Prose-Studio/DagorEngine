# JSON RPC over persistent websocket connections
if(WIN32)
  list(APPEND options /FC)
endif()

dagor_add_target(NAME gameLibs.websocketJsonRpc STATIC
  FILES_CMAKE websocketJsonRpc_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5 ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE engine.crypto gameLibs.websocket 3rdPartyLibs.arc.zstd-1.4.5
)
