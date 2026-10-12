# Quirrel FRP: observables (Watched, Computed) and their update graph, with an ImGui inspector
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
)
set(sources frp.cpp frp_imgui.cpp)
if(DAGOR_SQ_VAR_TRACE)
  list(APPEND defines SQ_VAR_TRACE_ENABLED)
endif()
if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_library(gameLibs.quirrel.frp ${sources})
target_include_directories(gameLibs.quirrel.frp PRIVATE ${includes})
target_compile_definitions(gameLibs.quirrel.frp PRIVATE ${defines})
target_compile_options(gameLibs.quirrel.frp PRIVATE ${options})
target_link_libraries(gameLibs.quirrel.frp PRIVATE Dagor::Quirrel)
