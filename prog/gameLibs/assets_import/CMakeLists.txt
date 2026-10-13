list(APPEND deps Dagor::Phys)
if(DAGOR_GAME_RENDERER)
  if(WIN32 AND DAGOR_GAME_ASSET_MANAGER)
    # jam built daBuild into the game for it (DabuildEmbeddedInGame) and the shaders with a second bindump
    message(FATAL_ERROR "gameLibs/assets_import: the in-game asset manager (DAGOR_GAME_ASSET_MANAGER) is not ported yet")
  endif()
endif()
dagor_add_dng_module(NAME gameLibs.assets_import DAS
  FILES_CMAKE assets_import_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/tools/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
