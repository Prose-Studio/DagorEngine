# TODO(jam): include $(Root)/prog/3rdPartyLibs/phys/bullet-$(BulletSdkVer)/setup.jam ;
# TODO(jam): include $(Root)/prog/3rdPartyLibs/phys/joltPhysics/setup.jam ;

dagor_add_target(NAME tools.AssetViewer.physObj STATIC LAX
  FILES_CMAKE physObj_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/phys/bullet-3/src
    ${DAGOR_PROG_DIR}/3rdPartyLibs/phys/joltPhysics
)
