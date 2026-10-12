# Primitive mesh generation for rendering: spheres, cylinders and cube indices
dagor_add_target(NAME gameLibs.render.primitiveObjects STATIC
  FILES_CMAKE primitiveObjects_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
