if(DAGOR_GAME_RENDERER)
  list(APPEND pull_vars auto_graphics_ui)
endif()
dagor_add_dng_module(NAME daNetGameLibs.auto_graphics
  FILES_CMAKE auto_graphics_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  BUILD_DEPENDENCIES PRIVATE gameLibs.render.autoGraphics
  PULL_VARS ${pull_vars}
)
