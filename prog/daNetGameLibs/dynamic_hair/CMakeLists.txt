set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME daNetGameLibs.dynamic_hair
  FILES_CMAKE dynamic_hair_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
