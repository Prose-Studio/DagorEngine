set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/libb64/include
)
set(AllSrcFolder_CPP .)
set(AllSrcFolder_ES .)

dagor_add_dng_module(gameLibs.dasModules.localization CPP_DIRS ${AllSrcFolder_CPP} ES_DIRS ${AllSrcFolder_ES})
target_include_directories(gameLibs.dasModules.localization PRIVATE ${includes})
