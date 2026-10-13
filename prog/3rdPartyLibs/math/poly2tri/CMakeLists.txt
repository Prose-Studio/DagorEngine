dagor_add_target(NAME 3rdPartyLibs.math.poly2tri STATIC LAX
  FILES_CMAKE poly2tri_files.cmake
  COMPILE_DEFINITIONS PRIVATE __B_NO_MEM_BASE_INCLUDE
)
