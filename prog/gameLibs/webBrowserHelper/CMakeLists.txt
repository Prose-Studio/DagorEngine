# The games' embedded browser (DAGOR_GAME_EMBEDDED_BROWSER): the browser of 1stPartyLibs.webbrowser, its view as a
# texture and its events to the scripts. The programs that link it get the CEF process and CEF's runtime next to them.
dagor_add_target(NAME gameLibs.webBrowserHelper STATIC
  FILES_CMAKE webBrowserHelper_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.webbrowser Dagor::Quirrel CEF::Runtime
)
add_dependencies(gameLibs.webBrowserHelper cefprocess)
set_property(TARGET gameLibs.webBrowserHelper APPEND PROPERTY
  INTERFACE_DAGOR_RUNTIME_FILES ".|$<TARGET_FILE:cefprocess>")
