set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources wakePs.cpp shipWakeFx.cpp)

dagor_add_library(gameLibs.render.wakePs ${sources})
target_include_directories(gameLibs.render.wakePs PRIVATE ${includes})
