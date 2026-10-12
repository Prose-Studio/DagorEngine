# Animated characters: the anim char (skeleton, anim graph state, physics), its rendering and the second animation
# pass. Programs with the DAGOR_MEASURE_PERF property get the build with profiling counters (MEASURE_PERF=1).
add_subdirectory(stub)

set(options)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-undefined-bool-conversion)
endif()
foreach(build standard measurePerf)
  set(defines)
  if(build STREQUAL "measurePerf")
    set(defines MEASURE_PERF=1)
  endif()
  dagor_add_library(engine.animChar.${build} animCharacter2.cpp animCharBase.cpp animCharRend.cpp animate2ndPass.cpp)
  target_include_directories(engine.animChar.${build} PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/acl/includes)
  target_compile_definitions(engine.animChar.${build} PRIVATE ${defines})
  target_compile_options(engine.animChar.${build} PRIVATE ${options})
  target_link_libraries(engine.animChar.${build} PRIVATE engine.anim engine.phys.fastPhys)
endforeach()
dagor_add_link_choice(engine.animChar PROPERTY DAGOR_MEASURE_PERF
  ON engine.animChar.measurePerf OFF engine.animChar.standard)
