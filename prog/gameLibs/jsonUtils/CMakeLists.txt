# JSON utilities: loading and saving rapidjson documents as files, JWT decoding
set(includes
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${DAGOR_PROG_DIR}/3rdPartyLibs/libb64/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
)
set(sources jsonUtils.cpp decodeJwt.cpp)
list(APPEND deps 1stPartyLibs.jsoncpp 1stPartyLibs.rapidJsonUtils)

dagor_add_library(gameLibs.jsonUtils ${sources})
target_include_directories(gameLibs.jsonUtils PRIVATE ${includes})
target_link_libraries(gameLibs.jsonUtils PRIVATE ${deps})
set_target_properties(gameLibs.jsonUtils PROPERTIES DAGOR_FRAME_LIMIT 262144)
