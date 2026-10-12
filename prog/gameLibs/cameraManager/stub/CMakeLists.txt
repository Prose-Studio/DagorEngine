# The camera manager of games without a renderer
dagor_add_library(gameLibs.cameraManager.stub cameraManagerStub.cpp)
target_include_directories(gameLibs.cameraManager.stub PRIVATE ${DAGOR_PROG_DIR}/gameLibs)
