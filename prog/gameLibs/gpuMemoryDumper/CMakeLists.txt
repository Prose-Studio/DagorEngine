dagor_add_target(NAME gameLibs.gpuMemoryDumper STATIC LAX
  FILES_CMAKE gpuMemoryDumper_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
)
