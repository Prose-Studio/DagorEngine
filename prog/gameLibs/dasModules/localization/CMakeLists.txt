dagor_add_dng_module(NAME gameLibs.dasModules.localization
  FILES_CMAKE localization_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/libb64/include
)
