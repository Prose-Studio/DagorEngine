dagor_add_target(NAME gameLibs.dasModules.perFrameStat STATIC
  FILES_CMAKE perFrameStat_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.daScript
)
