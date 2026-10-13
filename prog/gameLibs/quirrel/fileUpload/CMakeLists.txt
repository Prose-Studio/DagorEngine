dagor_add_target(NAME gameLibs.quirrel.fileUpload STATIC
  FILES_CMAKE fileUpload_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE gameLibs.quirrel.sqEventBus Dagor::Quirrel
)
