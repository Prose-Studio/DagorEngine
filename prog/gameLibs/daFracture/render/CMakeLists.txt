set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources renderContext.cpp renderList.cpp renderMesh.cpp unitedGeomBuffers.cpp material.cpp sceneRender.cpp)

dagor_add_library(gameLibs.daFracture.render ${sources})
target_include_directories(gameLibs.daFracture.render PRIVATE ${includes})
