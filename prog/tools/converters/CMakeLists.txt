# the dirs of prog/tools/converters
add_subdirectory(GuiTex)
add_subdirectory(ddsConverter)
add_subdirectory(ddsx2dds)
add_subdirectory(ddsxCvt)
if(DAGOR_KERNEL_LINKAGE STREQUAL "dynamic") # ddsxCvt2: the converter on daKernel, with the plugins
  add_subdirectory(ddsxCvt2)
endif()
