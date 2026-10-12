if(WIN32)
  list(APPEND options /wd4548)
endif()
if(DAGOR_DAS_AOT_COMPILER)
  list(APPEND defines DAS_AOT_COMPILER) # the AOT compiler's stubs (prog/gameLibs/dasModules/module_common.jam)
endif()

dagor_add_target(NAME gameLibs.dasModules.stdGui STATIC
  FILES_CMAKE stdGui_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.daScript
)
