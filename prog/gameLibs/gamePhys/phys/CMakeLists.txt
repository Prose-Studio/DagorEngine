dagor_add_target(NAME gameLibs.gamePhys.phys STATIC
  FILES_CMAKE phys_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
