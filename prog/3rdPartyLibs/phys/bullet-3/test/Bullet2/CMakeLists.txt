# Bullet's SIMD math (vectors, quaternions, 3x3 matrices, min/max dot products, btDbvt) checked against plain code
include(../bullet_test.cmake)
bullet_test(NAME bullet-3-Bullet2
  FILES_CMAKE Bullet2_files.cmake
  INCLUDE_DIRECTORIES PRIVATE Source Source/Tests
)
# every check of its list but btDbvt's: its Select check fails on ties (its random boxes often merge into one of the two
# they came from, and the SIMD Select and its reference pick different ones of two equal boxes)
set(checks maxdot mindot qtmul qtmulQV3 qtmulV3Q qtdot qtnorm v3dot v3sdiv v3norm v3cross v3triple v3interp v3lerp v3skew
  v3div v3rotate dot3 3x3transpose 3x3transposeTimes 3x3timesTranspose 3x3mulM 3x3mulM1M2 3x3mulMV 3x3mulVM 3x3setRot
  3x3getRot quat_aos_neon)
dagor_add_exec_test(3rdPartyLibs.bullet-3.Bullet2 COMMAND $<TARGET_FILE:bullet-3-Bullet2> ${checks} TAGS 3rdPartyLibs)
