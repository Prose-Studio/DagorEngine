dagor_add_target(NAME tools.sceneTools.daEditorX.services.carCamera STATIC LAX
  FILES_CMAKE carCamera_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/phys/bullet-3/src
  BUILD_DEPENDENCIES PRIVATE Dagor::BulletSettings
)
