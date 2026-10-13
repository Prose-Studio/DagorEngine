dagor_add_dng_module(NAME daNetGameLibs.water_ripples
  FILES_CMAKE water_ripples_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
