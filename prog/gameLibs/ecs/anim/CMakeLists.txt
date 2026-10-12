dagor_add_target(NAME gameLibs.ecs.anim STATIC
  FILES_CMAKE anim_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl gameLibs.render.animCharTexReplace
)
