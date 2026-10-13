dagor_add_dng_module(NAME gameLibs.animTreeEditor
  FILES_CMAKE animTreeEditor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.imgui tools.libTools.propPanel tools.libTools.winGuiWrapper
)
