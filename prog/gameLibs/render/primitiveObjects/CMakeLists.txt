# Primitive mesh generation for rendering: spheres, cylinders and cube indices
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources primitiveObjects.cpp)

dagor_add_library(gameLibs.render.primitiveObjects ${sources})
target_include_directories(gameLibs.render.primitiveObjects PRIVATE ${includes})
