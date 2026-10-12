set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources window.cpp)
list(APPEND deps 3rdPartyLibs.eastl)

dagor_add_library(gameLibs.ecs.os ${sources})
target_include_directories(gameLibs.ecs.os PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.os PRIVATE Dagor::Quirrel ${deps})
