# daNet delta compression (RLE, history buffers)
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

dagor_add_target(NAME engine.daNet.delta STATIC
  FILES_CMAKE delta_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.daNet
)
