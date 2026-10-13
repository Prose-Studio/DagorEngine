dagor_add_target(NAME gameLibs.ecs.anim STATIC
  FILES_CMAKE anim_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl gameLibs.render.animCharTexReplace
)
