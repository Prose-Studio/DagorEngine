# Quirrel JWT decoding module (on jsonUtils and digitalSignature)
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/libb64/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
)
set(sources sqJwt.cpp)
set(deps gameLibs.digitalSignature gameLibs.jsonUtils)

dagor_add_library(gameLibs.quirrel.sqJwt ${sources})
target_include_directories(gameLibs.quirrel.sqJwt PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqJwt PRIVATE Dagor::Quirrel ${deps})
