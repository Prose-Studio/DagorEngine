# The in-game asset manager (DAGOR_GAME_ASSET_MANAGER): daBuild built into the client builds the assets it loads and
# rebuilds them when they change; its daScript reloads them. Without it, the stub.
list(APPEND deps Dagor::Phys)
if(DAGOR_GAME_ASSET_MANAGER)
  list(APPEND deps tools.libTools.assetMgr tools.libTools.assetMgrHlp.emb tools.libTools.dtx tools.sceneTools.assetExp)
endif()
dagor_add_dng_module(NAME gameLibs.assets_import DAS
  FILES_CMAKE assets_import_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/tools/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
