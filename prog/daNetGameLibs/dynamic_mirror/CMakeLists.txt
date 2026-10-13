dagor_add_dng_module(NAME daNetGameLibs.dynamic_mirror
  FILES_CMAKE dynamic_mirror_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
