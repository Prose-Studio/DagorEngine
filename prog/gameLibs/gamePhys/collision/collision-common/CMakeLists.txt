# The game's collision (prog/gameLibs/gamePhys/collision/jamfile-General, built without APEX): the sources are in the
# parent dir
set(options)
dagor_deterministic_fp(options)

dagor_add_target(NAME gameLibs.gamePhys.collision.collision-common STATIC
  FILES_CMAKE collision-common_files.cmake
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys gameLibs.rendInst gameLibs.physMap gameLibs.fftWater
)
target_include_directories(gameLibs.gamePhys.collision.collision-common PRIVATE ${DAGOR_PROG_DIR}
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/engine/sharedInclude # gameRes/collisionResourceBuilder.h
)
target_compile_definitions(gameLibs.gamePhys.collision.collision-common PRIVATE VECMATH_NO_FMA # v_madd on NEON is explicit vfmaq that ignores ffp-contract=off
)
