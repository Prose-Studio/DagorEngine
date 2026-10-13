# The Quirrel host of the engine: memory allocation through the engine and memory tracing
if(DAGOR_SQ_VAR_TRACE)
  list(APPEND defines SQ_VAR_TRACE_ENABLED)
endif()

dagor_add_target(NAME gameLibs.quirrel.quirrelHost STATIC LAX
  FILES_CMAKE quirrelHost_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel/squirrel
    ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel/internal
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE Dagor::QuirrelHeaders
)
