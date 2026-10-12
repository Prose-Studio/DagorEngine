# Frustum planes as shader variables (set directly or by a scoped override)
dagor_add_target(NAME gameLibs.frustumCulling STATIC LAX
  FILES_CMAKE frustumCulling_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
