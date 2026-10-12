# ddsxCvt2: converts textures to DDSx with the asset manager's texture build settings (daKernel, the editor tree)
dagor_add_target(NAME ddsxCvt2 EXECUTABLE LAX
  FILES_CMAKE ddsxCvt2_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math tools.libTools.dtx tools.libTools.assetMgr tools.libTools.assetMgrHlp tools.libTools.util
    tools.libTools.daKernel
  CDK
)
