set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources forceFeedbackStub.cpp)

dagor_add_library(gameLibs.forceFeedback.stub ${sources})
target_include_directories(gameLibs.forceFeedback.stub PRIVATE ${includes})
