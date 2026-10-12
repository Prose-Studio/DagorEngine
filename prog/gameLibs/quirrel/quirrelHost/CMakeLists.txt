# The Quirrel host of the engine: memory allocation through the engine and memory tracing
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel/squirrel
  ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel/internal
)
set(sources memtrace.cpp sqmem_dagor.cpp)
# no reuse of freed blocks under ASan, which then sees use after free
if(DAGOR_SANITIZE STREQUAL "address")
  set_property(SOURCE sqmem_dagor.cpp APPEND PROPERTY COMPILE_OPTIONS -DENABLE_RE_USE=0)
endif()
if(DAGOR_SQ_VAR_TRACE)
  list(APPEND defines SQ_VAR_TRACE_ENABLED)
endif()

dagor_add_library(gameLibs.quirrel.quirrelHost LAX ${sources})
target_include_directories(gameLibs.quirrel.quirrelHost PRIVATE ${includes})
target_compile_definitions(gameLibs.quirrel.quirrelHost PRIVATE ${defines})
target_link_libraries(gameLibs.quirrel.quirrelHost PRIVATE Dagor::QuirrelHeaders)
