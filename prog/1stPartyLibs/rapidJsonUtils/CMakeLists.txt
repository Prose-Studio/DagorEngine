# RapidJSON helpers on EASTL: typed member get/set with error strings, key copies, stringify
dagor_add_target(NAME 1stPartyLibs.rapidJsonUtils STATIC LAX
  FILES_CMAKE rapidJsonUtils_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
