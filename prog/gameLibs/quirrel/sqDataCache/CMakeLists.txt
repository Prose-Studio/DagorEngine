dagor_add_target(NAME gameLibs.quirrel.sqDataCache STATIC
  FILES_CMAKE sqDataCache_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel gameLibs.datacache gameLibs.folders
)
