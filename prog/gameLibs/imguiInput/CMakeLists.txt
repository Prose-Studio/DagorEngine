dagor_add_target(NAME gameLibs.imguiInput STATIC LAX
  FILES_CMAKE imguiInput_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl 3rdPartyLibs.imgui engine.imgui gameLibs.daInput
)
