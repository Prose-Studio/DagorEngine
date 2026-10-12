add_subdirectory(common)
add_subdirectory(file)
add_subdirectory(web)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
list(APPEND deps gameLibs.datacache.common gameLibs.datacache.file gameLibs.datacache.web)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)

dagor_add_target(NAME gameLibs.datacache STATIC
  FILES_CMAKE datacache_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
