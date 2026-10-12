add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources enviCover.cpp enviCoverVars.cpp)

dagor_add_library(gameLibs.render.enviCover LAX ${sources})
target_include_directories(gameLibs.render.enviCover PRIVATE ${includes})
