dagor_add_target(NAME gameLibs.ecs.defaultAnimcharRender STATIC
  FILES_CMAKE defaultAnimcharRender_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
