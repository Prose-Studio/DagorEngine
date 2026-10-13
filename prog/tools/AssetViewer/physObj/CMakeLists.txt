# The physics objects of AssetViewer, on both physics engines
dagor_add_target(NAME tools.AssetViewer.physObj STATIC LAX
  FILES_CMAKE physObj_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/phys/bullet-3/src ${DAGOR_PROG_DIR}/3rdPartyLibs/phys/joltPhysics
  BUILD_DEPENDENCIES PRIVATE Dagor::BulletSettings Dagor::JoltSettings
)
