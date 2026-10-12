if(WIN32)
  list(APPEND options /wd4548)
endif()
list(APPEND deps 1stPartyLibs.daScript gameLibs.ecs.scripts.das)
list(APPEND deps Dagor::Phys)

dagor_add_target(NAME gameLibs.dasModules.rendInst STATIC
  FILES_CMAKE rendInst_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
