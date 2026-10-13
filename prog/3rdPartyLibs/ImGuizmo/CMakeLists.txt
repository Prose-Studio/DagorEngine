dagor_add_target(NAME 3rdPartyLibs.ImGuizmo STATIC LAX
  FILES_CMAKE ImGuizmo_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
)
