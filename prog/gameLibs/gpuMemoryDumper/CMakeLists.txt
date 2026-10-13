dagor_add_target(NAME gameLibs.gpuMemoryDumper STATIC LAX
  FILES_CMAKE gpuMemoryDumper_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
