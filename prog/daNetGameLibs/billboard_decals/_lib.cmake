if(DAGOR_GAME_RENDERER)
  dagor_game_lib(PULLS
    daNetGameLibs_billboard_decals_DAS_pull_AOT
    BillboardDecalsModule_pull
    framework_billboard_decals_pull
  )
  dagor_game_lib(LINK daNetGameLibs.billboard_decals)
endif()
