# Bullet's kinematic character controller (gtest)
include(../bullet_test.cmake)
bullet_test(NAME bullet-3-BulletDynamics
  FILES_CMAKE BulletDynamics_files.cmake
)
dagor_add_exec_test(3rdPartyLibs.bullet-3.BulletDynamics COMMAND $<TARGET_FILE:bullet-3-BulletDynamics> TAGS 3rdPartyLibs)
