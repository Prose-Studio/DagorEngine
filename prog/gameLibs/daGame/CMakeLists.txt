add_subdirectory(timers)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources netUnit.cpp)

dagor_add_library(gameLibs.daGame LAX ${sources})
target_include_directories(gameLibs.daGame PRIVATE ${includes})
