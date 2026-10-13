dagor_add_target(NAME 3rdPartyLibs.ImGuiColorTextEdit STATIC LAX
  FILES_CMAKE ImGuiColorTextEdit_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui ${DAGOR_PROG_DIR}/3rdPartyLibs/eastl/include
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.imgui
)
