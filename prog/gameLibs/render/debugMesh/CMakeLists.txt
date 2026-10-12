# Debug mesh coloring modes (the debug gbuffer modes, overdraw) and their console command
add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources debugMesh.cpp)

dagor_add_library(gameLibs.render.debugMesh ${sources})
target_include_directories(gameLibs.render.debugMesh PRIVATE ${includes})
