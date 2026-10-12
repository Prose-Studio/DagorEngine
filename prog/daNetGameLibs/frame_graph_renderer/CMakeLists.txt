dagor_add_dng_module(NAME daNetGameLibs.frame_graph_renderer DAS
  FILES_CMAKE frame_graph_renderer_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/render/daFrameGraph ${DAGOR_PROG_DIR}/daNetGame
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
)
