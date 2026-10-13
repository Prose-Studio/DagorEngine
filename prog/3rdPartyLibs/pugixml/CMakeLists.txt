dagor_add_target(NAME 3rdPartyLibs.pugixml STATIC LAX
  FILES_CMAKE pugixml_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/pugixml
)
