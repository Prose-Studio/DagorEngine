# findUnusedTex: on daKernel (the assets tree)
dagor_add_target(NAME findUnusedTex EXECUTABLE LAX
  FILES_CMAKE findUnusedTex_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math tools.libTools.dtx tools.libTools.util tools.libTools.assetMgr tools.libTools.assetMgrHlp
    tools.libTools.daKernel
  CDK
)
