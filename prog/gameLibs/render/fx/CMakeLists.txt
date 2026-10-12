# Render effects: bloom, UI blurring, post fx, aurora borealis, lightning, lens flares
dagor_add_target(NAME gameLibs.render.fx STATIC
  FILES_CMAKE fx_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
