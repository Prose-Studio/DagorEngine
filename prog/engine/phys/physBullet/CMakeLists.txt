# The engine's physics on Bullet (DAGOR_PHYS Bullet, the tools'; the libraries link it through Dagor::Phys)
dagor_add_target(NAME engine.phys.physBullet STATIC LAX
  FILES_CMAKE physBullet_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  COMPILE_DEFINITIONS PRIVATE USE_BULLET_PHYSICS
  BUILD_DEPENDENCIES PRIVATE engine.phys.physCommon 3rdPartyLibs.phys.bullet-3
)
