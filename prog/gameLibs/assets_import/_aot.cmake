# the asset manager's daScript module (DAGOR_GAME_ASSET_MANAGER, Windows clients), its daBuild stubbed
if(WIN32)
  dagor_game_lib(SOURCES dasModules/assets_import.cpp _aot/stub_assets_import.cpp
    INCLUDES ${DAGOR_ENGINE_ROOT}/prog/tools/sharedInclude ${DAGOR_ENGINE_ROOT}/prog/engine/sharedInclude)
endif()
