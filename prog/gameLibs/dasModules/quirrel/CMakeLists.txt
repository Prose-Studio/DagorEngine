if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_target(NAME gameLibs.dasModules.quirrel STATIC
  FILES_CMAKE quirrel_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/modules/dasQuirrel/src
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE
    Dagor::Quirrel 1stPartyLibs.daScript gameLibs.ecs.scripts.das 1stPartyLibs.daScript.modules.dasQuirrel
)
