dagor_add_target(NAME gameLibs.ecs.os STATIC
  FILES_CMAKE os_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel 3rdPartyLibs.eastl
)
