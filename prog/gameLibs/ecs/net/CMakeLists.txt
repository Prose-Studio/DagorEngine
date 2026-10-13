dagor_add_target(NAME gameLibs.ecs.net STATIC
  FILES_CMAKE net_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
