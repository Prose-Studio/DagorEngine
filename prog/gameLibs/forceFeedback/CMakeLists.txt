add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources rumble.cpp triggerEffect.cpp)

dagor_add_library(gameLibs.forceFeedback ${sources})
target_include_directories(gameLibs.forceFeedback PRIVATE ${includes})
