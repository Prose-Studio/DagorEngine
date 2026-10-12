set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources
  loc.cpp
  polares.cpp
  mass.cpp
  kinematics.cpp
  fixed_dt.cpp
  chainIKSolver.cpp
  constraintChainIKSolver.cpp
)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND LINUX AND DAGOR_ARCH STREQUAL "x86_64")
  set_property(SOURCE chainIKSolver.cpp APPEND PROPERTY COMPILE_OPTIONS -mno-avx2)
endif()

dagor_add_library(gameLibs.gamePhys.common ${sources})
target_include_directories(gameLibs.gamePhys.common PRIVATE ${includes})
