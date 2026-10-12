# The developer console: commands, variables, the console processor
dagor_add_target(NAME engine.consoleProc STATIC
  FILES_CMAKE consoleProc_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.imgui
)
