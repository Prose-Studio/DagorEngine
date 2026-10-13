dagor_add_target(NAME gameLibs.perFrameStat STATIC
  FILES_CMAKE perFrameStat_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.workCycle gameLibs.render
)
