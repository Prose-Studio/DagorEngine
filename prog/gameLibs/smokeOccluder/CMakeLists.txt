dagor_add_target(NAME gameLibs.smokeOccluder STATIC
  FILES_CMAKE smokeOccluder_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.daECS.core
)
