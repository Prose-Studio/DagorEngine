if(DAGOR_DAS_AOT) # the daslib scripts compiled ahead of time
  add_subdirectory(daslib)
endif()

set(includes
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
  ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui-node-editor
)
set(AllSrcFolder_CPP src)
dagor_glob_sources(sources DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
list(APPEND deps 3rdPartyLibs.eastl 1stPartyLibs.daScript 3rdPartyLibs.imgui 3rdPartyLibs.imgui-node-editor)
if(DAGOR_DAS_AOT)
  list(APPEND deps 1stPartyLibs.daScript.modules.dasImgui.daslib) # its daslib scripts, compiled ahead of time
endif()

dagor_add_library(1stPartyLibs.daScript.modules.dasImgui ${sources})
target_include_directories(1stPartyLibs.daScript.modules.dasImgui PRIVATE ${includes})
target_link_libraries(1stPartyLibs.daScript.modules.dasImgui PRIVATE ${deps})
