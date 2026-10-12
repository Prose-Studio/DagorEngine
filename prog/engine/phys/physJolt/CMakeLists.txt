# The engine's physics on Jolt (DAGOR_PHYS Jolt; the libraries link it through Dagor::Phys)
set(options)
dagor_deterministic_fp(options)

dagor_add_library(engine.phys.physJolt LAX joltPhysics.cpp joltPhysObject.cpp joltPhysRagdoll.cpp joltPhysSysInst.cpp
  joltDbgRender.cpp joltRayCar.cpp shapes/HeightField16Shape.cpp shapes/CollisionBlasShape.cpp
  shapes/FastCollideConvexVsTriangles.cpp)
target_include_directories(engine.phys.physJolt PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/phys/joltPhysics ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_compile_definitions(engine.phys.physJolt PRIVATE USE_JOLT_PHYSICS VECMATH_NO_FMA # v_madd on NEON is explicit vfmaq that ignores ffp-contract=off
)
target_compile_options(engine.phys.physJolt PRIVATE ${options})
target_link_libraries(engine.phys.physJolt PRIVATE engine.phys.physCommon 3rdPartyLibs.phys.joltPhysics
  engine.heightMapLand engine.gameRes # CollResJoltChunk shares a CollisionResource::Data block
  Dagor::JoltSettings)
