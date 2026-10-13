if(DAGOR_GAME_RENDERER)
  dagor_game_lib(PULLS framework_collimatorMoaCore_pull gameLibs_collimatorMoaCore_DAS_pull_AOT)
  dagor_game_lib(LINK gameLibs.render.collimatorMoaCore)
endif()
