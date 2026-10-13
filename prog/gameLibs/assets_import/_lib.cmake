if(DAGOR_GAME_RENDERER)
  dagor_game_lib(PULLS framework_assets_import_pull)
  dagor_game_lib(LINK gameLibs.assets_import)
  # the asset manager's daScript module and scripts, out of Rel
  if(DAGOR_GAME_ASSET_MANAGER)
    dagor_game_lib(PULLS "$<$<NOT:$<CONFIG:Rel>>:gameLibs_assets_import_DAS_pull_AOT>"
      "$<$<NOT:$<CONFIG:Rel>>:AssetsImportModule_pull>")
  endif()
endif()
