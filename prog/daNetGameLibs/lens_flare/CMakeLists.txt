if(DAGOR_GAME_RENDERER)
  list(APPEND deps gameLibs.render.lensFlare)
endif()
dagor_add_dng_module(NAME daNetGameLibs.lens_flare
  FILES_CMAKE lens_flare_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs
    ${DAGOR_PROG_DIR}/daNetGame
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
