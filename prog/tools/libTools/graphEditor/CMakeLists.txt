dagor_add_target(NAME tools.libTools.graphEditor STATIC LAX
  FILES_CMAKE graphEditor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui-node-editor
)
