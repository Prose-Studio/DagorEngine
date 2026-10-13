# the game's ImGui and daEditor tools, where the game has its editor (outside Rel)
if(DAGOR_GAME_RENDERER AND NOT DAGOR_GAME_EDITOR STREQUAL "0")
  dagor_game_lib(LINK "$<${DAGOR_GAME_EDITOR}:gameLibs.imgui_daeditor>"
    PULLS "$<${DAGOR_GAME_EDITOR}:gameLibs_imgui_daeditor_DAS_pull_AOT>")
endif()
