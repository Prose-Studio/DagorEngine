set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME daNetGameLibs.semi_trans_render
  FILES_CMAKE semi_trans_render_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
    ${DAGOR_PROG_DIR}/engine ${DAGOR_PROG_DIR}/engine/sharedInclude
)
