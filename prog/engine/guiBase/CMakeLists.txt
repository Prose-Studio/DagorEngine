dagor_add_target(NAME engine.guiBase STATIC
  FILES_CMAKE guiBase_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/freetype-2.8/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/harfbuzz-2.6.4/src ${DAGOR_PROG_DIR}/3rdPartyLibs/binPack2D/include
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.freetype.freetype-2.8 3rdPartyLibs.freetype.harfbuzz-2.6.4 3rdPartyLibs.binPack2D
)
