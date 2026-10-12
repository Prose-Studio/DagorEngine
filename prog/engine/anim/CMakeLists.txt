# Animation: blend trees, IK/FABRIK, post-blend controllers, the anim graph and its state. Programs with the
# DAGOR_MEASURE_PERF property get the build with profiling counters (MEASURE_PERF=1), as AssetViewer.
set(sources
  animBlendCtrl.cpp
  animPostBlendCtrl.cpp
  animIKCtrl.cpp
  animFABRIKCtrl.cpp
  animChannels.cpp
  animGraph.cpp
  animGraphDbg.cpp
  animStateHolder.cpp
  simpleNodeAnim.cpp
)
set(options)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-undefined-bool-conversion)
endif()
foreach(build standard measurePerf)
  set(defines)
  if(build STREQUAL "measurePerf")
    set(defines MEASURE_PERF=1)
  endif()
  dagor_add_library(engine.anim.${build} ${sources})
  target_include_directories(engine.anim.${build} PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/acl/includes)
  target_compile_definitions(engine.anim.${build} PRIVATE ${defines})
  target_compile_options(engine.anim.${build} PRIVATE ${options})
  target_link_libraries(engine.anim.${build} PRIVATE 3rdPartyLibs.regExp)
endforeach()
dagor_add_link_choice(engine.anim PROPERTY DAGOR_MEASURE_PERF ON engine.anim.measurePerf OFF engine.anim.standard)
