set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources customRendinstTrace.cpp)
list(APPEND deps gameLibs.landMesh)

dagor_add_library(gameLibs.gamePhys.collision.customRendinstTrace LAX ${sources})
target_include_directories(gameLibs.gamePhys.collision.customRendinstTrace PRIVATE ${includes})
target_link_libraries(gameLibs.gamePhys.collision.customRendinstTrace PRIVATE ${deps})
