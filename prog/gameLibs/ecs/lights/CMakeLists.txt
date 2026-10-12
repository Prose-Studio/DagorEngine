dagor_add_target(NAME gameLibs.ecs.lights STATIC
  FILES_CMAKE lights_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
