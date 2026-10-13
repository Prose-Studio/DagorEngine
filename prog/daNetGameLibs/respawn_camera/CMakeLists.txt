dagor_add_dng_module(NAME daNetGameLibs.respawn_camera
  FILES_CMAKE respawn_camera_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
