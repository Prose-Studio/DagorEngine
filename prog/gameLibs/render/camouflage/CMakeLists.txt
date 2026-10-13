dagor_add_target(NAME gameLibs.render.camouflage STATIC
  FILES_CMAKE camouflage_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
