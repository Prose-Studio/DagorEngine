dagor_add_target(NAME gameLibs.quirrel.sqDebugConfig STATIC
  FILES_CMAKE sqDebugConfig_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
