# Volumetric lights (VolumeLight) stubs for programs without volumetric lighting
set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources volumetricLightsStub.cpp)

dagor_add_library(gameLibs.render.volumetricLights.stub LAX ${sources})
target_include_directories(gameLibs.render.volumetricLights.stub PRIVATE ${includes})
