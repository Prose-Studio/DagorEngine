# Software ray tracing BVHs: SAH BLAS building, quad/SoA4 leaf encodings, serialization, the TLAS and CPU traversal
dagor_add_target(NAME engine.daBVH STATIC
  FILES_CMAKE daBVH_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} shaders
)
