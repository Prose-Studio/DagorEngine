# Bullet 3's OpenCL: device initialization and the compile and launch of its kernels (gtest). Not a CTest test: it
# needs an OpenCL runtime and device.
include(../bullet_test.cmake)
bullet_test(NAME bullet-3-TestBullet3OpenCL
  FILES_CMAKE TestBullet3OpenCL_files.cmake
)
