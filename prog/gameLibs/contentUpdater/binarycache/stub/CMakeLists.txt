dagor_add_target(NAME gameLibs.contentUpdater.binarycache.stub STATIC
  FILES_CMAKE stub_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
