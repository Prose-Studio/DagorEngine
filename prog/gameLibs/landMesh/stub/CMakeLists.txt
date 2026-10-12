set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources landMeshStub.cpp)

dagor_add_library(gameLibs.landMesh.stub ${sources})
target_include_directories(gameLibs.landMesh.stub PRIVATE ${includes})
