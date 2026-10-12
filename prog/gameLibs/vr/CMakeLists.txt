set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources vrGuiSurface.cpp vrHands.cpp)
list(APPEND deps Dagor::Phys)

dagor_add_library(gameLibs.vr ${sources})
target_include_directories(gameLibs.vr PRIVATE ${includes})
target_link_libraries(gameLibs.vr PRIVATE ${deps})
