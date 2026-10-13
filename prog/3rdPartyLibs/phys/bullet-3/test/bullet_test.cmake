# bullet_test(NAME <name> <dagor_add_target arguments>): a console test program of Bullet, with gtest, the engine's
# kernel on the RTL allocator and Bullet's own aligned allocator (bullet_test_files.cmake: the engine's build of
# Bullet leaves it to engine.phys.physBullet); included by the test dirs
include_guard(GLOBAL)
function(bullet_test)
  set(options)
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    list(APPEND options -Wno-format -Wno-undefined-inline)
    if(MSVC)
      list(APPEND options -fp:fast)
      if(NOT DAGOR_ARCH STREQUAL "arm64")
        list(APPEND options /clang:-fno-unsafe-math-optimizations)
      endif()
    else()
      list(APPEND options -ffast-math -fno-unsafe-math-optimizations)
    endif()
  endif()
  dagor_add_target(${ARGN} EXECUTABLE LAX
    FILES_CMAKE ${CMAKE_CURRENT_FUNCTION_LIST_DIR}/bullet_test_files.cmake
    COMPILE_OPTIONS PRIVATE ${options}
    BUILD_DEPENDENCIES PRIVATE
      engine.memory.rtl engine.kernel engine.ioSys engine.osApiWrappers engine.baseUtil engine.perfMon.daProfilerStub
      3rdPartyLibs.eastl 3rdPartyLibs.phys.bullet-3 3rdPartyLibs.phys.bullet-3.test.gtest-1.7.0
  )
endfunction()
