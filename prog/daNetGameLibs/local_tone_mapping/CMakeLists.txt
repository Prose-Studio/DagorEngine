dagor_add_dng_module(NAME daNetGameLibs.local_tone_mapping DAS
  FILES_CMAKE local_tone_mapping_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/gameLibs/render/daFrameGraph
)
