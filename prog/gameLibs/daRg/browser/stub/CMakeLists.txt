set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources uiBehaviorBinding.cpp)

dagor_add_library(gameLibs.daRg.browser.stub ${sources})
target_include_directories(gameLibs.daRg.browser.stub PRIVATE ${includes})
target_link_libraries(gameLibs.daRg.browser.stub PRIVATE Dagor::Quirrel)
