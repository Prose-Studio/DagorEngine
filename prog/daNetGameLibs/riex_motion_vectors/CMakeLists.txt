dagor_add_dng_module(NAME daNetGameLibs.riex_motion_vectors
  FILES_CMAKE riex_motion_vectors_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
