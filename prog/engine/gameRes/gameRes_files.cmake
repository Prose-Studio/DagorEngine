set(FILES
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
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND DAGOR_ARCH STREQUAL "e2k")
  set_property(SOURCE collisionGameRes.cpp APPEND PROPERTY COMPILE_OPTIONS -Wno-pass-failed)
endif()
if(DAGOR_LTO AND CMAKE_CXX_COMPILER_ID STREQUAL "MSVC" AND DAGOR_ARCH STREQUAL "arm64")
  set_property(SOURCE collisionGameRes.cpp APPEND PROPERTY COMPILE_OPTIONS /GL-) # MSVC's arm64 LTO miscompiles it
endif()
