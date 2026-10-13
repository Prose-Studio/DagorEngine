# Debug rendering of game primitives (lines, shapes, text); the debug drawing itself outside Rel, never in a dedicated
# server
dagor_add_target(NAME gameLibs.gameDebugRender STATIC
  FILES_CMAKE gameDebugRender_files.cmake
)
