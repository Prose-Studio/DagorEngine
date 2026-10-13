dagor_add_target(NAME 3rdPartyLibs.netImguiServer STATIC LAX
  FILES_CMAKE netImguiServer_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui ${DAGOR_PROG_DIR}/3rdPartyLibs/netImgui
    ${DAGOR_PROG_DIR}/3rdPartyLibs/stb ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.netImgui 3rdPartyLibs.arc.zstd-1.4.5
)
