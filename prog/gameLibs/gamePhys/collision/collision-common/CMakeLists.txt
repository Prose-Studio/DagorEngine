# The game's collision (prog/gameLibs/gamePhys/collision/jamfile-General, built without APEX): the sources are in the
# parent dir
set(options)
dagor_deterministic_fp(options)

dagor_add_library(gameLibs.gamePhys.collision.collision-common ../collisionResponse.cpp ../collisionLib.cpp
  ../collisionInstances.cpp ../rendinstCollision.cpp ../traceLib.cpp ../collisionLinks.cpp ../contactSolver.cpp
  ../collisionCache.cpp)
target_include_directories(gameLibs.gamePhys.collision.collision-common PRIVATE ${DAGOR_PROG_DIR}
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/engine/sharedInclude # gameRes/collisionResourceBuilder.h
)
target_compile_definitions(gameLibs.gamePhys.collision.collision-common PRIVATE VECMATH_NO_FMA # v_madd on NEON is explicit vfmaq that ignores ffp-contract=off
)
target_compile_options(gameLibs.gamePhys.collision.collision-common PRIVATE ${options})
target_link_libraries(gameLibs.gamePhys.collision.collision-common PRIVATE Dagor::Phys gameLibs.rendInst
  gameLibs.physMap gameLibs.fftWater)
