dagor_add_target(NAME gameLibs.gamePhys.collision.rendinst STATIC
  FILES_CMAKE rendinst_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
