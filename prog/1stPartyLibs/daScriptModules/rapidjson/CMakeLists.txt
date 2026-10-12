dagor_add_target(NAME 1stPartyLibs.daScriptModules.rapidjson STATIC LAX
  FILES_CMAKE rapidjson_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  LICENSES ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson
)
