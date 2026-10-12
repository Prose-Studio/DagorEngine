# Math: vectors and matrices, frustums, geometry queries, noise, DXT decompression. Programs with the
# DAGOR_MEASURE_PERF property get the build with profiling counters (MEASURE_PERF=1), as AssetViewer.
set(defines)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "static" AND WIN32)
  list(APPEND defines _DEBUG_TAB_)
endif()

foreach(build standard measurePerf)
  set(build_defines ${defines})
  if(build STREQUAL "measurePerf")
    list(APPEND build_defines MEASURE_PERF=1)
  endif()
  dagor_add_target(NAME engine.math.${build} STATIC
    FILES_CMAKE math_files.cmake
    COMPILE_DEFINITIONS PRIVATE ${build_defines}
    BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
  )
endforeach()
dagor_add_link_choice(engine.math PROPERTY DAGOR_MEASURE_PERF ON engine.math.measurePerf OFF engine.math.standard)
