set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
)
set(sources nestdb.cpp)
if(DAGOR_SQ_VAR_TRACE)
  list(APPEND defines SQ_VAR_TRACE_ENABLED)
endif()
if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_library(gameLibs.quirrel.nestdb ${sources})
target_include_directories(gameLibs.quirrel.nestdb PRIVATE ${includes})
target_compile_definitions(gameLibs.quirrel.nestdb PRIVATE ${defines})
target_compile_options(gameLibs.quirrel.nestdb PRIVATE ${options})
target_link_libraries(gameLibs.quirrel.nestdb PRIVATE Dagor::Quirrel)
