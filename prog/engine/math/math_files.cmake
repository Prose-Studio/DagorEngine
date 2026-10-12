set(FILES
  convexHullComputer.cpp
  half.cpp
  calc_occluder.cpp
  colorMatrix.cpp
  boundingSphere.cpp
  math3d.cpp
  math2d.cpp
  frustum.cpp
  mathAng.cpp
  perlin.cpp
  ffd44.cpp
  triangleTriangleIntersection.cpp
  sHmath.cpp
  geomTree.cpp
  geomTreeMap.cpp
  mesh.cpp
  mathUtils.cpp
  kaiserSimd.cpp
  imageFunctions.cpp
  polyUtils.cpp
  capsuleTriangle.cpp
  wooray2d.cpp
  wooray3d.cpp
  checkNanTest.cpp
  sdf_edt.cpp
)
if(DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND FILES dxtDecompressSimd.cpp)
else()
  list(APPEND FILES dxtDecompress.cpp)
endif()
if(DAGOR_KERNEL_LINKAGE STREQUAL "static")
  list(APPEND FILES rndSeed.cpp gaussTbl.cpp)
endif()
