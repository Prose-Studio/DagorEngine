set(Source )

dagor_add_target(NAME gameLibs.ecs.camera STATIC
  FILES_CMAKE camera_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
