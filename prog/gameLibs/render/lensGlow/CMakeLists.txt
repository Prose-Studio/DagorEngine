set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME gameLibs.render.lensGlow
  FILES_CMAKE lensGlow_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
