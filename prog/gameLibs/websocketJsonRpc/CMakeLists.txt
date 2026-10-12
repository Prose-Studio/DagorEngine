# JSON RPC over persistent websocket connections
add_subdirectory(tests)

list(APPEND includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
)
list(APPEND deps engine.crypto gameLibs.websocket 3rdPartyLibs.arc.zstd-1.4.5)
set(AllSrcFolder_CPP .)
dagor_glob_sources(sources DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
if(WIN32)
  list(APPEND options /FC)
endif()

dagor_add_library(gameLibs.websocketJsonRpc ${sources})
target_include_directories(gameLibs.websocketJsonRpc PRIVATE ${includes})
target_compile_options(gameLibs.websocketJsonRpc PRIVATE ${options})
target_link_libraries(gameLibs.websocketJsonRpc PRIVATE ${deps})
