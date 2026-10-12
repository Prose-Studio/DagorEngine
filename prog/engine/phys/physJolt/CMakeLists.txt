# The engine's physics on Jolt (DAGOR_PHYS Jolt; the libraries link it through Dagor::Phys)
set(options)
dagor_deterministic_fp(options)

dagor_add_target(NAME engine.phys.physJolt STATIC LAX
  FILES_CMAKE physJolt_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/phys/joltPhysics
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  COMPILE_OPTIONS PRIVATE ${options}
)
target_compile_definitions(engine.phys.physJolt PRIVATE USE_JOLT_PHYSICS VECMATH_NO_FMA # v_madd on NEON is explicit vfmaq that ignores ffp-contract=off
)
target_link_libraries(engine.phys.physJolt PRIVATE engine.phys.physCommon 3rdPartyLibs.phys.joltPhysics
  engine.heightMapLand engine.gameRes # CollResJoltChunk shares a CollisionResource::Data block
  Dagor::JoltSettings)
