# The engine's physics on Bullet (DAGOR_PHYS Bullet, the tools'; the libraries link it through Dagor::Phys)
dagor_add_library(engine.phys.physBullet LAX bulletPhysics.cpp bulletPhysObject.cpp bulletPhysRagdoll.cpp
  bulletPhysSysInst.cpp bulletLoadPhysScene.cpp bulletRayCar.cpp bulletAlloc.cpp bulletDbgRender.cpp
  btDagorHeightfieldTerrainShape.cpp)
target_include_directories(engine.phys.physBullet PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_compile_definitions(engine.phys.physBullet PRIVATE USE_BULLET_PHYSICS)
target_link_libraries(engine.phys.physBullet PRIVATE engine.phys.physCommon 3rdPartyLibs.phys.bullet-3)
