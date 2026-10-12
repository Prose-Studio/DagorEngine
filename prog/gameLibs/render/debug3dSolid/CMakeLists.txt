# Debug drawing of solid shapes (meshes, spheres, capsules, cubes, cones), immediate and buffered with a lifetime
add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources debug3dSolid.cpp debug3dSolidBuffered.cpp)

dagor_add_library(gameLibs.render.debug3dSolid ${sources})
target_include_directories(gameLibs.render.debug3dSolid PRIVATE ${includes})
