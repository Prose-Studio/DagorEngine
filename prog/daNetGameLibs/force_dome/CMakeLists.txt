set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME daNetGameLibs.force_dome
  FILES_CMAKE force_dome_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
