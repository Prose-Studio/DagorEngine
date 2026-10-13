# JSON utilities: loading and saving rapidjson documents as files, JWT decoding
dagor_add_target(NAME gameLibs.jsonUtils STATIC
  FILES_CMAKE jsonUtils_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/3rdPartyLibs/libb64/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.jsoncpp 1stPartyLibs.rapidJsonUtils
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
