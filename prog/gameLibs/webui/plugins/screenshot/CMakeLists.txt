dagor_add_target(NAME gameLibs.webui.plugins.screenshot STATIC
  FILES_CMAKE screenshot_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/webui ${DAGOR_PROG_DIR}/dagorInclude
  BUILD_DEPENDENCIES PRIVATE engine.screenShotSystem
)
