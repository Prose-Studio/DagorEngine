dagor_add_dng_module(NAME daNetGameLibs.initial_transform_cache
  FILES_CMAKE initial_transform_cache_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
