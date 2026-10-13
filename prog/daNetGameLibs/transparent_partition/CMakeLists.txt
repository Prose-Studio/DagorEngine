dagor_add_dng_module(NAME daNetGameLibs.transparent_partition
  FILES_CMAKE transparent_partition_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
