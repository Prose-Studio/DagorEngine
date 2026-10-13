dagor_add_target(NAME gameLibs.textureGen STATIC
  FILES_CMAKE textureGen_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl 3rdPartyLibs.hash gameLibs.webui.plugins.editorCurves
)
