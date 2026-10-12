# Stub of the GPU object placing parameters of the ECS rendInst code for programs without it
set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources preparePlacingParameters.cpp)

dagor_add_library(gameLibs.ecs.rendInst.stub ${sources})
target_include_directories(gameLibs.ecs.rendInst.stub PRIVATE ${includes})
