dagor_add_dng_module(NAME daNetGameLibs.screen_night_vision DAS
  FILES_CMAKE screen_night_vision_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
    ${DAGOR_PROG_DIR}/gameLibs/render/daFrameGraph
)
