dagor_add_target(NAME gameLibs.datacache STATIC
  FILES_CMAKE datacache_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  BUILD_DEPENDENCIES PRIVATE
    gameLibs.datacache.common gameLibs.datacache.file gameLibs.datacache.web 3rdPartyLibs.openssl-3.x
)
