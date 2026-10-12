set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources rendinstCollisionWrapper.cpp rendinstCollisionUserInfo.cpp rendinstContactResultWrapper.cpp)
list(APPEND deps Dagor::Phys)

dagor_add_library(gameLibs.gamePhys.collision.rendinst ${sources})
target_include_directories(gameLibs.gamePhys.collision.rendinst PRIVATE ${includes})
target_link_libraries(gameLibs.gamePhys.collision.rendinst PRIVATE ${deps})
