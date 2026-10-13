dagor_add_dng_module(NAME daNetGameLibs.nbs_volumes
  FILES_CMAKE nbs_volumes_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
