set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME daNetGameLibs.bloom
  FILES_CMAKE bloom_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
    ${DAGOR_PROG_DIR}/gameLibs
  BUILD_DEPENDENCIES PRIVATE gameLibs.render.bloomCore
)
