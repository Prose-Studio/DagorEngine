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
  dagor_add_target(NAME engine.animChar.${build} STATIC
    FILES_CMAKE animChar_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/acl/includes
    COMPILE_DEFINITIONS PRIVATE ${defines}
    COMPILE_OPTIONS PRIVATE ${options}
    BUILD_DEPENDENCIES PRIVATE engine.anim engine.phys.fastPhys
  )
endforeach()
dagor_add_link_choice(engine.animChar PROPERTY DAGOR_MEASURE_PERF
  ON engine.animChar.measurePerf OFF engine.animChar.standard)
