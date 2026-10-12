# ImGui helpers: BLK editing, strings, images, a filtered combo box
include(../netImgui.cmake)
dagor_add_target(NAME engine.imgui.util STATIC LAX
  FILES_CMAKE util_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${NET_IMGUI_INCLUDES}
  COMPILE_DEFINITIONS PRIVATE ${NET_IMGUI_DEFINES}
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.imgui ${NET_IMGUI_DEPS}
)
