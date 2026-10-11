# the daScript ImGui module's scripts compiled ahead of time (DAGOR_DAS_AOT), which the module links then
dagor_add_library(STRICT
  PRIVATE_INCLUDES ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  DAS_AOT imgui_boost.das imgui_node_editor_boost.das DAS_AOT_PULL daslib_imgui_DAS_pull_AOT
  LICENSE_FILES ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/modules/dasImgui/LICENSE
)
