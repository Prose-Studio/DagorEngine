# the daScript ImGui module's scripts compiled ahead of time (DAGOR_DAS_AOT), which the module links then
dagor_add_target(NAME 1stPartyLibs.daScript.modules.dasImgui.daslib STATIC
  FILES_CMAKE daslib_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  LICENSES ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/modules/dasImgui/LICENSE
  DAS_PULL daslib_imgui_DAS_pull_AOT
)
