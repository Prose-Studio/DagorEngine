# The ImGui input handling where there is none (the dedicated servers). It does not link engine/imgui/stub, which its
# programs never use: they all link engine/imgui. With both, the link order
# would mix the two, so it is not linked here; the code needs nothing of engine/imgui.
dagor_add_target(NAME gameLibs.imguiInput.stub STATIC LAX
  FILES_CMAKE stub_files.cmake
)
