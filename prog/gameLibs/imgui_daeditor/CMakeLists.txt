# The ImGui and daEditor tools of daScript games (DAS): the anim graph, rendinst and editor windows.
# outside Rel only; their daScript is compiled ahead of time in every configuration, loaded where the game has them.
dagor_add_dng_module(NAME gameLibs.imgui_daeditor DAS
  FILES_CMAKE imgui_daeditor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
