dagor_add_target(NAME gameLibs.contentUpdater.binarycache STATIC
  FILES_CMAKE binarycache_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
