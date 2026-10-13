# netImgui's remote ImGui client for the engine: the library itself on PCs (the consoles had their network code here)
dagor_add_target(NAME engine.imgui.netImgui HEADERONLY
  BUILD_DEPENDENCIES INTERFACE 3rdPartyLibs.netImgui
)
