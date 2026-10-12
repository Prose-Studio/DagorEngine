# The dynamic model renderer: per-instance render data of dynmodels and animchars for render contexts
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources dynmodelRenderer.cpp animCharRenderAdditionalData.cpp)

dagor_add_library(gameLibs.render.dynmodelRenderer ${sources})
target_include_directories(gameLibs.render.dynmodelRenderer PRIVATE ${includes})
