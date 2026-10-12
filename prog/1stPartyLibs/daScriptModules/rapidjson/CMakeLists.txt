dagor_add_library(1stPartyLibs.daScriptModules.rapidjson LAX jsonWriter.cpp rapidjson.cpp)
target_include_directories(1stPartyLibs.daScriptModules.rapidjson PRIVATE
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include)
dagor_target_licenses(1stPartyLibs.daScriptModules.rapidjson ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson)
