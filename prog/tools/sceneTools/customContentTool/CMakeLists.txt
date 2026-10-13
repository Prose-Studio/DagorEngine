# customContentTool: on daKernel (the assets tree)
dagor_add_target(NAME customContentTool EXECUTABLE LAX
  FILES_CMAKE customContentTool_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math engine.coreUtil tools.libTools.dtx tools.libTools.assetMgr tools.libTools.assetMgrHlp
    tools.libTools.util 3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.openssl-3.x tools.libTools.daKernel
  CDK
)
