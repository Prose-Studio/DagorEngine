# The ImGui input handling where there is none (the dedicated servers). jam also linked engine/imgui/stub, which its
# programs never used: they all link engine/imgui, which came first in jam's link order. With both, CMake's order
# would mix the two, so it is not linked here; the code needs nothing of engine/imgui.
dagor_add_library(gameLibs.imguiInput.stub LAX imguiInput_stub.cpp)
target_include_directories(gameLibs.imguiInput.stub PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
