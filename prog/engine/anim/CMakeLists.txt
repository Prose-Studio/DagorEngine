# Animation: blend trees, IK/FABRIK, post-blend controllers, the anim graph and its state. Programs with the
# DAGOR_MEASURE_PERF property get the build with profiling counters (MEASURE_PERF=1), as AssetViewer.
set(options)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-undefined-bool-conversion)
endif()
foreach(build standard measurePerf)
  set(defines)
  if(build STREQUAL "measurePerf")
    set(defines MEASURE_PERF=1)
  endif()
  dagor_add_target(NAME engine.anim.${build} STATIC
    FILES_CMAKE anim_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/acl/includes
    COMPILE_DEFINITIONS PRIVATE ${defines}
    COMPILE_OPTIONS PRIVATE ${options}
    BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.regExp
  )
endforeach()
dagor_add_link_choice(engine.anim PROPERTY DAGOR_MEASURE_PERF ON engine.anim.measurePerf OFF engine.anim.standard)
