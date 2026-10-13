dagor_add_target(NAME gameLibs.webvromfs STATIC
  FILES_CMAKE webvromfs_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  BUILD_DEPENDENCIES PRIVATE gameLibs.datacache 3rdPartyLibs.openssl-3.x
)
