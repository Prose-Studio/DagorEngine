# Hooks for the land classes of rendInsts used by the land mesh (rendInst land class and detail data)
dagor_add_target(NAME gameLibs.landMesh.rendinstIntegration STATIC LAX
  FILES_CMAKE rendinstIntegration_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
