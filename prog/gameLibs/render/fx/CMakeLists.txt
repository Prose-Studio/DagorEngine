# Render effects: bloom, UI blurring, post fx, aurora borealis, lightning, lens flares
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources
  bloom_ps.cpp
  ui_blurring.cpp
  blurredUI.cpp
  demonPostFx.cpp
  postfx.cpp
  auroraBorealis.cpp
  lightning.cpp
  flare.cpp
)

dagor_add_library(gameLibs.render.fx ${sources})
target_include_directories(gameLibs.render.fx PRIVATE ${includes})
set_target_properties(gameLibs.render.fx PROPERTIES DAGOR_FRAME_LIMIT 262144)
