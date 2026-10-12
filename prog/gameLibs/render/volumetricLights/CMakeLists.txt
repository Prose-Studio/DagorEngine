add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources volumetricLights.cpp)

dagor_add_library(gameLibs.render.volumetricLights LAX ${sources})
target_include_directories(gameLibs.render.volumetricLights PRIVATE ${includes})
