dagor_add_target(NAME gameLibs.quirrel.sqPerFrameStat STATIC
  FILES_CMAKE sqPerFrameStat_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel gameLibs.perFrameStat
)
