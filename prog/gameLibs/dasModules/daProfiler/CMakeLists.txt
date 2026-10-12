if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_target(NAME gameLibs.dasModules.daProfiler STATIC
  FILES_CMAKE daProfiler_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.daScript engine.perfMon gameLibs.folders
)
