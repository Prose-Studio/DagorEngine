set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel)
set(sources sqWebBrowser.cpp)

dagor_add_library(gameLibs.quirrel.sqWebBrowser.stub ${sources})
target_include_directories(gameLibs.quirrel.sqWebBrowser.stub PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqWebBrowser.stub PRIVATE Dagor::Quirrel)
