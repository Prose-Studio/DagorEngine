add_subdirectory(destrRenderStub)
add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(AllSrcFolder . rendInstDestr)
dagor_glob_sources(sources DIRS ${AllSrcFolder} GLOB *.cpp)
list(APPEND deps Dagor::Phys)

dagor_add_library(gameLibs.gamePhys.phys ${sources})
target_include_directories(gameLibs.gamePhys.phys PRIVATE ${includes})
target_link_libraries(gameLibs.gamePhys.phys PRIVATE ${deps})
