# netImgui (remote ImGui) for the engine's ImGui libraries, outside Rel: sets
# NET_IMGUI_DEFINES, NET_IMGUI_INCLUDES and NET_IMGUI_DEPS
set(NET_IMGUI_DEFINES)
set(NET_IMGUI_INCLUDES)
set(NET_IMGUI_DEPS)
if(DAGOR_NET_IMGUI AND CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows|iOS)$")
  set(NET_IMGUI_DEFINES "$<$<NOT:$<CONFIG:Rel>>:ADD_NET_IMGUI>")
  set(NET_IMGUI_INCLUDES ${DAGOR_PROG_DIR}/3rdPartyLibs/netImgui ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5)
  set(NET_IMGUI_DEPS "$<$<NOT:$<CONFIG:Rel>>:3rdPartyLibs.netImgui>" "$<$<NOT:$<CONFIG:Rel>>:3rdPartyLibs.arc.zstd-1.4.5>")
endif()
