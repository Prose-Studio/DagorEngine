dagor_add_target(NAME gameLibs.gamePhys.phys.stub STATIC
  FILES_CMAKE stub_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
