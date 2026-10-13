# Static scenes: tiled scenes, visibility trees, occlusion maps, level loading, ray tracer dumps, physical materials
dagor_add_target(NAME engine.scene STATIC LAX
  FILES_CMAKE scene_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
