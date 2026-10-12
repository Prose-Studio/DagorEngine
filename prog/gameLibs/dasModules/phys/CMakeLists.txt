if(WIN32)
  list(APPEND options /wd4548)
endif()
set(deps 1stPartyLibs.daScript)
list(APPEND deps Dagor::Phys)

dagor_add_target(NAME gameLibs.dasModules.phys STATIC
  FILES_CMAKE phys_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
