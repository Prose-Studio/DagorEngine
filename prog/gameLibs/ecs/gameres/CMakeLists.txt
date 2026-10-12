dagor_add_target(NAME gameLibs.ecs.gameres STATIC
  FILES_CMAKE gameres_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
