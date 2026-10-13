dagor_add_target(NAME gameLibs.ecs.rendInst STATIC
  FILES_CMAKE rendInst_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl gameLibs.rendInst Dagor::Phys
)
