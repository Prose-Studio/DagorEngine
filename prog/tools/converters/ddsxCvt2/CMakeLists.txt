# ddsxCvt2: converts textures to DDSx with the asset manager's texture build settings (daKernel, the editor tree)
dagor_add_executable(ddsxCvt2 LAX ddsxConverter2.cpp con_main.cpp)
target_include_directories(ddsxCvt2 PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/engine/sharedInclude)
target_link_libraries(ddsxCvt2 PRIVATE engine.startup engine.math tools.libTools.dtx tools.libTools.assetMgr
  tools.libTools.assetMgrHlp tools.libTools.util tools.libTools.daKernel)
dagor_install_cdk(ddsxCvt2)
