if(DAGOR_GAME_RENDERER)
  list(APPEND pull_vars tiled_map_ui_bhv_sq)
endif()
dagor_add_dng_module(NAME daNetGameLibs.tiled_map
  FILES_CMAKE tiled_map_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  PULL_VARS ${pull_vars}
)
