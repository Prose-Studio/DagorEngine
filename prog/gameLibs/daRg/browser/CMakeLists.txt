# daRg's browser behavior and render object, on the games' embedded browser (DAGOR_GAME_EMBEDDED_BROWSER; stub/
# without it)
dagor_add_target(NAME gameLibs.daRg.browser STATIC
  FILES_CMAKE browser_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE gameLibs.webBrowserHelper Dagor::Quirrel
)
