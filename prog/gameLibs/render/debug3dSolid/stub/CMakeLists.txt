set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources debug3dSolidStub.cpp)

dagor_add_library(gameLibs.render.debug3dSolid.stub ${sources})
target_include_directories(gameLibs.render.debug3dSolid.stub PRIVATE ${includes})
