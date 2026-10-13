set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME daNetGameLibs.effect_area
  FILES_CMAKE effect_area_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
