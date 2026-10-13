dagor_add_target(NAME gameLibs.webui.plugins.profiler STATIC
  FILES_CMAKE profiler_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/webui
)
