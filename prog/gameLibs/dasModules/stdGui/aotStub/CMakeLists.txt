if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_target(NAME gameLibs.dasModules.stdGui.aotStub STATIC
  FILES_CMAKE aotStub_files.cmake
  COMPILE_OPTIONS PRIVATE ${options}
)
