dagor_add_target(NAME engine.daECS.hierarchyTransform STATIC
  FILES_CMAKE hierarchyTransform_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
