# Multi-line debug text labels (a gameLibs module): the stub without the renderer
if(DAGOR_GAME_RENDERER)
  set(cpp_dirs .)
  set(deps gameLibs.render gameLibs.hudprim)
else()
  set(cpp_dirs stub)
  set(deps)
endif()
dagor_add_dng_module(gameLibs.render.debugMultiTextLabels CPP_DIRS ${cpp_dirs})
target_include_directories(gameLibs.render.debugMultiTextLabels PRIVATE ${DAGOR_PROG_DIR}/gameLibs
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_link_libraries(gameLibs.render.debugMultiTextLabels PRIVATE ${deps})
