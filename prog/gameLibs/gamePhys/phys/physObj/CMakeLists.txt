dagor_add_target(NAME gameLibs.gamePhys.phys.physObj STATIC
  FILES_CMAKE physObj_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.gamePhys.phys gameLibs.gamePhys.props Dagor::Phys
)
