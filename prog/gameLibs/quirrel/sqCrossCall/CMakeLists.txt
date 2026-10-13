# Copying Quirrel values and calls between two Quirrel VMs
dagor_add_target(NAME gameLibs.quirrel.sqCrossCall STATIC
  FILES_CMAKE sqCrossCall_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
