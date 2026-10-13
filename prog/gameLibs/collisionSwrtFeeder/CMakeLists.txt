dagor_add_target(NAME gameLibs.collisionSwrtFeeder STATIC
  FILES_CMAKE collisionSwrtFeeder_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.daSWRT engine.daBVH
)
