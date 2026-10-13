dagor_add_target(NAME gameLibs.quirrel.sqSysInfo STATIC
  FILES_CMAKE sqSysInfo_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel gameLibs.userSystemInfo
)
