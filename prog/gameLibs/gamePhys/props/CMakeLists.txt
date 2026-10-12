add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources
  atmosphere.cpp
  shakeMatProps.cpp
  deformMatProps.cpp
  arcadeBoostProps.cpp
  softMaterialProps.cpp
  physMatDamageModelProps.cpp
  physDestructibleProps.cpp
  physContactProps.cpp
)

dagor_add_library(gameLibs.gamePhys.props ${sources})
target_include_directories(gameLibs.gamePhys.props PRIVATE ${includes})
