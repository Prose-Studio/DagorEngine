set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR})
set(sources collisionStub.cpp)
list(APPEND deps Dagor::Phys)

dagor_add_library(gameLibs.gamePhys.collision.stub ${sources})
target_include_directories(gameLibs.gamePhys.collision.stub PRIVATE ${includes})
target_link_libraries(gameLibs.gamePhys.collision.stub PRIVATE ${deps})
