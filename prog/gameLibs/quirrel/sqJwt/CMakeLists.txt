# Quirrel JWT decoding module (on jsonUtils and digitalSignature)
dagor_add_target(NAME gameLibs.quirrel.sqJwt STATIC
  FILES_CMAKE sqJwt_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/libb64/include ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel gameLibs.digitalSignature gameLibs.jsonUtils
)
