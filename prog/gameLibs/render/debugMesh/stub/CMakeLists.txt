# Debug mesh coloring stubs for programs without it
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources debugMesh.cpp)

dagor_add_library(gameLibs.render.debugMesh.stub ${sources})
target_include_directories(gameLibs.render.debugMesh.stub PRIVATE ${includes})
