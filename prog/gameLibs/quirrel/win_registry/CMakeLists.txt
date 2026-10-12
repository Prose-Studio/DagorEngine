# Quirrel bindings of the Windows registry (value reads and writes)
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel)
set(sources win_registry.cpp)

dagor_add_library(gameLibs.quirrel.win_registry ${sources})
target_include_directories(gameLibs.quirrel.win_registry PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.win_registry PRIVATE Dagor::Quirrel)
