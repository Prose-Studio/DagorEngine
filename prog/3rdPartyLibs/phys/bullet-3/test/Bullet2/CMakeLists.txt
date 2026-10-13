# Bullet's SIMD math (vectors, quaternions, 3x3 matrices, min/max dot products, btDbvt) checked against plain code
include(../bullet_test.cmake)
bullet_test(NAME bullet-3-Bullet2
  FILES_CMAKE Bullet2_files.cmake
  INCLUDE_DIRECTORIES PRIVATE Source Source/Tests
)
dagor_add_exec_test(3rdPartyLibs.bullet-3.Bullet2 COMMAND $<TARGET_FILE:bullet-3-Bullet2> TAGS 3rdPartyLibs)
