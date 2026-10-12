# daNet delta compression (RLE, history buffers)
dagor_add_target(NAME engine.daNet.delta STATIC
  FILES_CMAKE delta_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.daNet
)
