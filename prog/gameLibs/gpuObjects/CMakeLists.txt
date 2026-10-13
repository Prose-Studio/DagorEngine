# GPU objects: the GPU placement of small objects on surfaces (rendinst decorations), with the volume placer ES
dagor_add_target(NAME gameLibs.gpuObjects STATIC
  FILES_CMAKE gpuObjects_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
