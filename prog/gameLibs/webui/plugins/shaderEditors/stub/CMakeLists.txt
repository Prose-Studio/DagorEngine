set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude)
set(sources shaderEditorsStub.cpp)

dagor_add_library(gameLibs.webui.plugins.shaderEditors.stub ${sources})
target_include_directories(gameLibs.webui.plugins.shaderEditors.stub PRIVATE ${includes})
