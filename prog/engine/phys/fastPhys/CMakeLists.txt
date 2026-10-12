# Fast physics: the simple point-mass and constraint simulation of character details (cloth, hair, chains). Programs
# with the DAGOR_MEASURE_PERF property get the build with profiling counters (MEASURE_PERF=1).
foreach(build standard measurePerf)
  set(defines)
  if(build STREQUAL "measurePerf")
    set(defines MEASURE_PERF=1)
  endif()
  dagor_add_target(NAME engine.phys.fastPhys.${build} STATIC LAX
    FILES_CMAKE fastPhys_files.cmake
    COMPILE_DEFINITIONS PRIVATE ${defines}
  )
endforeach()
dagor_add_link_choice(engine.phys.fastPhys PROPERTY DAGOR_MEASURE_PERF
  ON engine.phys.fastPhys.measurePerf OFF engine.phys.fastPhys.standard)
