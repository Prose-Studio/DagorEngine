dagor_add_target(NAME gameLibs.quirrel.udp STATIC LAX
  FILES_CMAKE udp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel/squirrel
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
