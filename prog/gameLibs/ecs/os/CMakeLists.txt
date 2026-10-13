dagor_add_target(NAME gameLibs.ecs.os STATIC
  FILES_CMAKE os_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel 3rdPartyLibs.eastl
)
