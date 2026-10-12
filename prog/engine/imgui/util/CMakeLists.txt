# ImGui helpers: BLK editing, strings, images, a filtered combo box
include(../netImgui.cmake)
dagor_add_library(engine.imgui.util LAX imguiBlk.cpp imguiMisc.cpp imguiString.cpp imguiImage.cpp
  imguiComboWithFilter.cpp)
target_include_directories(engine.imgui.util PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${NET_IMGUI_INCLUDES})
target_compile_definitions(engine.imgui.util PRIVATE ${NET_IMGUI_DEFINES})
target_link_libraries(engine.imgui.util PRIVATE 3rdPartyLibs.imgui ${NET_IMGUI_DEPS})
