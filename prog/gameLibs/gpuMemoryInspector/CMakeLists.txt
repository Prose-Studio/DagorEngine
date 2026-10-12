set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
  ${CMAKE_CURRENT_SOURCE_DIR}
)
set(sources gpuMemoryInspector.cpp)

dagor_add_library(gameLibs.gpuMemoryInspector LAX ${sources})
target_include_directories(gameLibs.gpuMemoryInspector PRIVATE ${includes})
