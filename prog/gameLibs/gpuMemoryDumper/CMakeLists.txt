set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources gpuMemoryDumper.cpp)

dagor_add_library(gameLibs.gpuMemoryDumper LAX ${sources})
target_include_directories(gameLibs.gpuMemoryDumper PRIVATE ${includes})
