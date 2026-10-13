dagor_add_target(NAME gameLibs.quirrel.clientLog STATIC
  FILES_CMAKE clientLog_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
