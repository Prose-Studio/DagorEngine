# Debug drawing of solid shapes (meshes, spheres, capsules, cubes, cones), immediate and buffered with a lifetime
dagor_add_target(NAME gameLibs.render.debug3dSolid STATIC
  FILES_CMAKE debug3dSolid_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
