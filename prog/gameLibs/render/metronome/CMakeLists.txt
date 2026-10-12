# Metronome: frame pacing measurements on top of daFrameGraph
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources metronome.cpp)

dagor_add_library(gameLibs.render.metronome ${sources})
target_include_directories(gameLibs.render.metronome PRIVATE ${includes})
