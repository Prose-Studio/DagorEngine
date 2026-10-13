dagor_add_target(NAME 3rdPartyLibs.phys.bullet-3.Extras.ConvexDecomposition STATIC LAX
  FILES_CMAKE ConvexDecomposition_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::BulletSettings
)
