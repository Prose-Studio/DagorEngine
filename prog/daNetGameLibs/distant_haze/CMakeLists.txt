set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME daNetGameLibs.distant_haze
  FILES_CMAKE distant_haze_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
