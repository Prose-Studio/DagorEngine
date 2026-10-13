# Quirrel FRP: observables (Watched, Computed) and their update graph, with an ImGui inspector
if(DAGOR_SQ_VAR_TRACE)
  list(APPEND defines SQ_VAR_TRACE_ENABLED)
endif()
if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_target(NAME gameLibs.quirrel.frp STATIC
  FILES_CMAKE frp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
