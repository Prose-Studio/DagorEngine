if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_target(NAME gameLibs.dasModules.render STATIC
  FILES_CMAKE render_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.daScript
)
