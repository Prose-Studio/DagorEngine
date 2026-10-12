# Node based shader manager stubs: no scripted shader compilation or loading
set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources nodeBasedShaderManagerStub.cpp)

dagor_add_library(gameLibs.nodeBasedShaderManager.stub ${sources})
target_include_directories(gameLibs.nodeBasedShaderManager.stub PRIVATE ${includes})
