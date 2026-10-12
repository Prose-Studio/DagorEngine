# ImGui integration stubs: the engine's imgui_* API with ImGui always off
dagor_add_target(NAME engine.imgui.stub STATIC LAX
  FILES_CMAKE stub_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.imgui
)
