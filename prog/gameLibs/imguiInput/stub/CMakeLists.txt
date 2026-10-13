# The ImGui input handling where there is none (the dedicated servers). jam also linked engine/imgui/stub, which its
# programs never used: they all link engine/imgui, which came first in jam's link order. With both, CMake's order
# would mix the two, so it is not linked here; the code needs nothing of engine/imgui.
dagor_add_target(NAME gameLibs.imguiInput.stub STATIC LAX
  FILES_CMAKE stub_files.cmake
)
