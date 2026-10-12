dagor_add_target(NAME gameLibs.perFrameStat STATIC
  FILES_CMAKE perFrameStat_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE engine.workCycle gameLibs.render
)
