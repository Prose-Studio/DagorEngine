# webui: the programs' HTTP server for the browser tools, with its plugins
add_subdirectory(plugins)
add_subdirectory(stub)
add_subdirectory(websocket)

set(plugins colorpicker dagor dargMcp editvar grapheditor profiler screenshot shadervars quirrel)
if(CMAKE_SYSTEM_NAME STREQUAL "tvOS")
  list(APPEND plugins tvOS)
endif()
list(TRANSFORM plugins PREPEND gameLibs.webui.plugins.)

dagor_add_target(NAME gameLibs.webui STATIC
  FILES_CMAKE webui_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${plugins}
)
target_include_directories(gameLibs.webui PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/engine/sharedInclude # for access to the shaders' implementation
)
