set(Source )

dagor_add_target(NAME gameLibs.ecs.camera STATIC
  FILES_CMAKE camera_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
