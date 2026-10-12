add_subdirectory(stub)

dagor_add_target(NAME gameLibs.imguiInput STATIC LAX
  FILES_CMAKE imguiInput_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl 3rdPartyLibs.imgui engine.imgui gameLibs.daInput
)
