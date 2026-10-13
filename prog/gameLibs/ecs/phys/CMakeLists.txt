dagor_add_target(NAME gameLibs.ecs.phys STATIC
  FILES_CMAKE phys_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl Dagor::Phys
)
