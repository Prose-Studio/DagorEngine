dagor_add_target(NAME gameLibs.smokeOccluder STATIC
  FILES_CMAKE smokeOccluder_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE engine.daECS.core
)
