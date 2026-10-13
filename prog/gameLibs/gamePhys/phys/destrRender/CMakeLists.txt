dagor_add_target(NAME gameLibs.gamePhys.phys.destrRender STATIC
  FILES_CMAKE destrRender_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
