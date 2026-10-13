dagor_add_dng_module(NAME daNetGameLibs.burnt_ground
  FILES_CMAKE burnt_ground_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs
    ${DAGOR_PROG_DIR}/daNetGame
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
