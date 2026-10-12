# Multi-line debug text labels (a gameLibs module): the stub without the renderer
set(deps)
if(DAGOR_GAME_RENDERER)
  set(deps gameLibs.render gameLibs.hudprim)
endif()
dagor_add_dng_module(NAME gameLibs.render.debugMultiTextLabels
  FILES_CMAKE debugMultiTextLabels_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
