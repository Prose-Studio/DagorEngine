set(dirs)
if(DAGOR_GAME_RENDERER)
  set(dirs render)
endif()
dagor_add_dng_module(daNetGameLibs.render_debug DAS CPP_DIRS ${dirs} ES_DIRS ${dirs} DAS_DIRS ${dirs})
if(DAGOR_GAME_RENDERER)
  set_property(TARGET daNetGameLibs.render_debug APPEND PROPERTY INTERFACE_DAGOR_GAME_PULLS
    debug_indoor_probe_boxes_console_handler_pull gpu_driven_debug_renderer_pull)
endif()
target_include_directories(daNetGameLibs.render_debug PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include)
