# Tools texture library: DDS conversion and saving (on nvtt 2.0.7), DDSx plugins, texture names, RGBE images
set(deps engine.image 3rdPartyLibs.convert.nvtt-2.0.7 3rdPartyLibs.image.jpeg-6b 3rdPartyLibs.image.avif)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps 3rdPartyLibs.arc.lzma-9.20)
endif()

dagor_add_target(NAME tools.libTools.dtx STATIC LAX
  FILES_CMAKE dtx_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/nvtt-2.0.7 ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
