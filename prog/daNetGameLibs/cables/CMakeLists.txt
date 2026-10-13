set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame)
if(DAGOR_GAME_RENDERER)
  list(APPEND includes ${DAGOR_PROG_DIR}/daNetGameLibs/renderer/includes)
endif()
dagor_add_dng_module(NAME daNetGameLibs.cables
  FILES_CMAKE cables_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
)
