dagor_add_target(NAME 3rdPartyLibs.jsoncpp STATIC LAX
  FILES_CMAKE jsoncpp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/jsoncpp/include
)
