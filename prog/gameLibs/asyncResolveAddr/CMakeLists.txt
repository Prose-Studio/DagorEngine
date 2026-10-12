set(includes ${DAGOR_PROG_DIR}/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources asyncResolveAddr.cpp)

dagor_add_library(gameLibs.asyncResolveAddr ${sources})
target_include_directories(gameLibs.asyncResolveAddr PRIVATE ${includes})
