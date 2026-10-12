dagor_add_target(NAME gameLibs.quirrel.sqConsole STATIC
  FILES_CMAKE sqConsole_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
