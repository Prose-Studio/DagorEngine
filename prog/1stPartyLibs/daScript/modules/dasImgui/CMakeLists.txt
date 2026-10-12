list(APPEND deps 3rdPartyLibs.eastl 1stPartyLibs.daScript 3rdPartyLibs.imgui 3rdPartyLibs.imgui-node-editor)
if(DAGOR_DAS_AOT)
  list(APPEND deps 1stPartyLibs.daScript.modules.dasImgui.daslib) # its daslib scripts, compiled ahead of time
endif()

dagor_add_target(NAME 1stPartyLibs.daScript.modules.dasImgui STATIC
  FILES_CMAKE dasImgui_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
    ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui-node-editor
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
