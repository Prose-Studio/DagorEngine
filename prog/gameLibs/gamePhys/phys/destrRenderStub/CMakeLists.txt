set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources destructablesStub.cpp)
list(APPEND deps Dagor::Phys)

dagor_add_library(gameLibs.gamePhys.phys.destrRenderStub ${sources})
target_include_directories(gameLibs.gamePhys.phys.destrRenderStub PRIVATE ${includes})
target_link_libraries(gameLibs.gamePhys.phys.destrRenderStub PRIVATE ${deps})
