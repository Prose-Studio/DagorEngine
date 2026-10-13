dagor_add_target(NAME gameLibs.render.gpuBenchmark STATIC
  FILES_CMAKE gpuBenchmark_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
