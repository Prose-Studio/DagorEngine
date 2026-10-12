set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(deps gameLibs.datacache)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)

dagor_add_target(NAME gameLibs.webvromfs STATIC
  FILES_CMAKE webvromfs_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
