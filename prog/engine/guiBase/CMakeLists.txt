set(sources
  font.cpp
  imgui_drawlist.cpp
  stdGuiRender.cpp
  guiRenderCache.cpp
  cursorLite.cpp
  guiVars.cpp
  baseGuiStartup.cpp
  visConsole.cpp
  textMarks.cpp
  visualLog.cpp
  visualErr.cpp
  visMemReport.cpp
)
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/freetype-2.8/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/harfbuzz-2.6.4/src
  ${DAGOR_PROG_DIR}/3rdPartyLibs/binPack2D/include
)
set(deps 3rdPartyLibs.freetype.freetype-2.8 3rdPartyLibs.freetype.harfbuzz-2.6.4 3rdPartyLibs.binPack2D)

dagor_add_library(engine.guiBase ${sources})
target_include_directories(engine.guiBase PRIVATE ${includes})
target_link_libraries(engine.guiBase PRIVATE ${deps})
