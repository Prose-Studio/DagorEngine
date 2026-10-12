dagor_add_dng_module(NAME daNetGameLibs.render_debug DAS
  FILES_CMAKE render_debug_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
)
if(DAGOR_GAME_RENDERER)
  set_property(TARGET daNetGameLibs.render_debug APPEND PROPERTY INTERFACE_DAGOR_GAME_PULLS
    debug_indoor_probe_boxes_console_handler_pull gpu_driven_debug_renderer_pull)
endif()
