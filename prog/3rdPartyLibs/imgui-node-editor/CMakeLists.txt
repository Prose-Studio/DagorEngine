# imgui-node-editor: node graph widgets for ImGui
dagor_add_target(NAME 3rdPartyLibs.imgui-node-editor STATIC LAX
  FILES_CMAKE imgui-node-editor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.imgui
)
