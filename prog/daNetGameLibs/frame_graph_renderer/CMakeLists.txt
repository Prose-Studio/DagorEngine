set(das)
if(DAGOR_GAME_RENDERER)
  set(das render)
endif()
dagor_add_dng_module(daNetGameLibs.frame_graph_renderer DAS DAS_DIRS ${das})
target_include_directories(daNetGameLibs.frame_graph_renderer PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/render/daFrameGraph ${DAGOR_PROG_DIR}/daNetGame
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
