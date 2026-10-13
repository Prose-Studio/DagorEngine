if(DAGOR_GAME_RENDERER)
  list(APPEND deps gameLibs.render.lensGlow)
endif()
dagor_add_dng_module(NAME daNetGameLibs.lens_glow
  FILES_CMAKE lens_glow_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
    ${DAGOR_PROG_DIR}/gameLibs
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
