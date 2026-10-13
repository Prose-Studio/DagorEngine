dagor_add_target(NAME engine.imgui.netImguiServer STATIC LAX
  FILES_CMAKE netImguiServer_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui ${DAGOR_PROG_DIR}/3rdPartyLibs/netImgui
    ${DAGOR_PROG_DIR}/3rdPartyLibs/netImguiServer ${DAGOR_PROG_DIR}/3rdPartyLibs/stb
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5
  BUILD_DEPENDENCIES PRIVATE engine.imgui 3rdPartyLibs.netImgui 3rdPartyLibs.netImguiServer 3rdPartyLibs.arc.zstd-1.4.5
)
