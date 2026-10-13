dagor_add_target(NAME gameLibs.gpuMemoryInspector STATIC LAX
  FILES_CMAKE gpuMemoryInspector_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui ${CMAKE_CURRENT_SOURCE_DIR}
)
