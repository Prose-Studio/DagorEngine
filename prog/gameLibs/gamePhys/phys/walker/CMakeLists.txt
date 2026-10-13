dagor_add_target(NAME gameLibs.gamePhys.phys.walker STATIC
  FILES_CMAKE walker_files.cmake
  COMPILE_DEFINITIONS PRIVATE DISABLE_SYNC_DEBUG # the fork has no gameLibs/syncDebug
  BUILD_DEPENDENCIES PRIVATE gameLibs.gamePhys.phys gameLibs.gamePhys.props Dagor::Phys
)
