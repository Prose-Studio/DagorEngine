set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/webui
  ${DAGOR_PROG_DIR}/dagorInclude
)
set(sources screenshotPlugin.cpp)
set(deps engine.screenShotSystem)

dagor_add_library(gameLibs.webui.plugins.screenshot ${sources})
target_include_directories(gameLibs.webui.plugins.screenshot PRIVATE ${includes})
target_link_libraries(gameLibs.webui.plugins.screenshot PRIVATE ${deps})
