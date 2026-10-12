set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources physStub.cpp)
list(APPEND deps Dagor::Phys)

dagor_add_library(gameLibs.gamePhys.phys.stub ${sources})
target_include_directories(gameLibs.gamePhys.phys.stub PRIVATE ${includes})
target_link_libraries(gameLibs.gamePhys.phys.stub PRIVATE ${deps})
