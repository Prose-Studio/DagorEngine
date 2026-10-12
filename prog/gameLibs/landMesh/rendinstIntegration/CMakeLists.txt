# Hooks for the land classes of rendInsts used by the land mesh (rendInst land class and detail data)
set(sources riLandClass.cpp)
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)

dagor_add_library(gameLibs.landMesh.rendinstIntegration LAX ${sources})
target_include_directories(gameLibs.landMesh.rendinstIntegration PRIVATE ${includes})
