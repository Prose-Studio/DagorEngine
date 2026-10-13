set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME daNetGameLibs.timelapse_screener
  FILES_CMAKE timelapse_screener_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
