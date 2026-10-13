# Bullet's collision: sphere-sphere distance through GJK/EPA and MPR, heightfield triangles (gtest)
include(../bullet_test.cmake)
bullet_test(NAME bullet-3-collision
  FILES_CMAKE collision_files.cmake
)
dagor_add_exec_test(3rdPartyLibs.bullet-3.collision COMMAND $<TARGET_FILE:bullet-3-collision> TAGS 3rdPartyLibs)
