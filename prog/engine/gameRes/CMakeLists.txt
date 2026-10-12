# Game resources: the resource packs (grp), their descriptions and loading, the factories of the resource types
set(sources
  gameResSystem.cpp
  gameResPackList.cpp
  gameResHooks.cpp
  gameResDescBin.cpp
  gameResOptionalPacks.cpp
  a2d_gameres.cpp
  animCharGameRes.cpp
  characterGameRes.cpp
  dynModelGameRes.cpp
  effectGameRes.cpp
  fastPhysGameRes.cpp
  geomNodeTreeGameRes.cpp
  physObjGameRes.cpp
  physSysGameRes.cpp
  rendInstGameRes.cpp
  materialGameRes.cpp
  lshaderGameRes.cpp
  impostorDataGameRes.cpp
  collisionDebug.cpp
  collisionFactory.cpp
  collisionGameRes.cpp
  collisionGameResLoad.cpp
  collisionResourceBuilder.cpp
  collisionResourceInstance.cpp
  collisionTraceOOL.cpp
  stubGameResFactories.cpp
  collResDump.cpp
  legacy_sceneray.cpp
)
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)
list(APPEND deps 3rdPartyLibs.eastl engine.daBVH)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-undefined-bool-conversion)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND DAGOR_ARCH STREQUAL "e2k")
  set_property(SOURCE collisionGameRes.cpp APPEND PROPERTY COMPILE_OPTIONS -Wno-pass-failed)
endif()
if(DAGOR_LTO AND CMAKE_CXX_COMPILER_ID STREQUAL "MSVC" AND DAGOR_ARCH STREQUAL "arm64")
  set_property(SOURCE collisionGameRes.cpp APPEND PROPERTY COMPILE_OPTIONS /GL-) # MSVC's arm64 LTO miscompiles it
endif()

dagor_add_library(engine.gameRes ${sources})
target_include_directories(engine.gameRes PRIVATE ${includes})
target_compile_options(engine.gameRes PRIVATE ${options})
target_link_libraries(engine.gameRes PRIVATE ${deps})
set_target_properties(engine.gameRes PROPERTIES DAGOR_FRAME_LIMIT 262144)
