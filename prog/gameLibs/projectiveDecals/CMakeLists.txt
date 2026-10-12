set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources
  defaultDecalData.cpp
  projectiveDecals.cpp
  projectiveDecalsBuffer.cpp
  resizableProjectiveDecals.cpp
  ringBufferProjectiveDecals.cpp
)
list(APPEND deps engine.lib3d gameLibs.render)

dagor_add_library(gameLibs.projectiveDecals ${sources})
target_include_directories(gameLibs.projectiveDecals PRIVATE ${includes})
target_link_libraries(gameLibs.projectiveDecals PRIVATE ${deps})
