# BVH ray tracing (DAGOR_GAME_BVH), or its stub. The parts of the scene it covers are features, each with its stub;
# DAGOR_BVH_STUBS lists those a tree builds as stubs (a game's: DagorGame.cmake).
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include)
if(NOT DAGOR_GAME_BVH)
  dagor_add_target(NAME gameLibs.bvh STATIC
    FILES_CMAKE bvh_stub_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${includes}
    BUILD_DEPENDENCIES PRIVATE gameLibs.userSystemInfo gameLibs.eventLog
  )
  return()
endif()

# <feature> is bvh_<feature>.cpp, or stub/bvh_stub_<feature>.cpp (bvh_files.cmake); ri has more
set(features terrain ri dyn gobj grass cables bin_scene fft_water dagdp gpu_grass splinegen fx lru_collision
  smoke_tracers)
foreach(stub IN LISTS DAGOR_BVH_STUBS)
  if(NOT stub IN_LIST features)
    message(FATAL_ERROR "DAGOR_BVH_STUBS: no BVH feature '${stub}' (the features: ${features})")
  endif()
endforeach()
set(deps gameLibs.userSystemInfo gameLibs.eventLog gameLibs.render.omm)
if(NOT "lru_collision" IN_LIST DAGOR_BVH_STUBS)
  list(APPEND deps gameLibs.render.lruCollision)
endif()
set(options)
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  list(APPEND options /wd4582 /wd5031)
endif()

dagor_add_target(NAME gameLibs.bvh STATIC
  FILES_CMAKE bvh_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
