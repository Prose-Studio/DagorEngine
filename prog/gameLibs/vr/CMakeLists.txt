dagor_add_target(NAME gameLibs.vr STATIC
  FILES_CMAKE vr_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
