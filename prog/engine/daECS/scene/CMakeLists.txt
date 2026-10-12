dagor_add_target(NAME engine.daECS.scene STATIC
  FILES_CMAKE scene_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.daECS.io.datablock engine.daECS.core 3rdPartyLibs.eastl
)
