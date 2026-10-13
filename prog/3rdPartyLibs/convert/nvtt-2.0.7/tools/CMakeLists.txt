# NVIDIA Texture Tools' command-line tools (nvcompress, nvdecompress, nvassemble, nvddsinfo, nvimgdiff, nvzoom), into
# out/ next to them as jam built them
foreach(tool nvcompress nvdecompress nvassemble nvddsinfo nvimgdiff nvzoom)
  dagor_add_target(NAME ${tool} EXECUTABLE LAX NO_CONFIG_POSTFIX
    OUTPUT_DIRECTORY out
    FILES_CMAKE ${tool}_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/nvtt-2.0.7
    COMPILE_DEFINITIONS PRIVATE WIN32 _WINDOWS _USRDLL NVTT_EXPORTS __SSE2__ __SSE__ __MMX__
    BUILD_DEPENDENCIES PRIVATE
      engine.osApiWrappers engine.kernel engine.memory engine.baseUtil 3rdPartyLibs.convert.nvtt-2.0.7
      3rdPartyLibs.image.jpeg-6b 3rdPartyLibs.eastl
  )
endforeach()
