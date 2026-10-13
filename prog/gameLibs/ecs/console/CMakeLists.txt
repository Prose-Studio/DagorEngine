dagor_add_target(NAME gameLibs.ecs.console STATIC
  FILES_CMAKE console_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/consoleProc
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
