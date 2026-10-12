# netImgui: ImGui drawn remotely over the network
if(WIN32)
  list(APPEND defines NETIMGUI_WINSOCKET_ENABLED)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux)$")
  list(APPEND defines NETIMGUI_POSIX_SOCKETS_ENABLED)
endif()

dagor_add_target(NAME 3rdPartyLibs.netImgui STATIC LAX
  FILES_CMAKE netImgui_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} nlohmann_json quicklz ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
    ${DAGOR_PROG_DIR}/3rdPartyLibs/stb ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.imgui 3rdPartyLibs.arc.zstd-1.4.5
)
