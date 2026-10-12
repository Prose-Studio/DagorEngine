set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources webuiStub.cpp ../bson.cpp)

dagor_add_library(gameLibs.webui.stub ${sources})
target_include_directories(gameLibs.webui.stub PRIVATE ${includes})
