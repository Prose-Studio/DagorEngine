set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME daNetGameLibs.custom_envi_probe
  FILES_CMAKE custom_envi_probe_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
