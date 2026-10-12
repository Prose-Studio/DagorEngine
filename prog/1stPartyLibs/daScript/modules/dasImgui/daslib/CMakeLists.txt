# the daScript ImGui module's scripts compiled ahead of time (DAGOR_DAS_AOT), which the module links then
dagor_add_library(1stPartyLibs.daScript.modules.dasImgui.daslib)
target_include_directories(1stPartyLibs.daScript.modules.dasImgui.daslib PRIVATE
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
dagor_target_licenses(1stPartyLibs.daScript.modules.dasImgui.daslib
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/modules/dasImgui/LICENSE)
dagor_target_das_aot(1stPartyLibs.daScript.modules.dasImgui.daslib PULL daslib_imgui_DAS_pull_AOT imgui_boost.das
  imgui_node_editor_boost.das)
