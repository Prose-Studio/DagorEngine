dagor_add_dng_module(NAME daNetGameLibs.screen_droplets
  FILES_CMAKE screen_droplets_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
