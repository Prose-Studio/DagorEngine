dagor_add_target(NAME 3rdPartyLibs.phys.bullet-3.Extras.InverseDynamics STATIC LAX
  FILES_CMAKE InverseDynamics_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::BulletSettings
)
