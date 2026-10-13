if(DAGOR_GAME_RENDERER)
  dagor_game_lib(PULLS
    framework_motionMatching_pull
    gameLibs_motionMatching_DAS_pull_AOT
    MotionMatchingModule_pull
  )
  dagor_game_lib(LINK gameLibs.anim.motionMatching)
endif()
dagor_game_lib(PULLS FootLockerIKCtrl_pull)
dagor_game_lib(LINK gameLibs.anim.footLockerIKCtrl)
