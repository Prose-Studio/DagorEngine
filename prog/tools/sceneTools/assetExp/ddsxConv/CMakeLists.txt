# The DDSx texture converter plugins of daBuild and the tools (plugins/ddsx): pcDdsxConv (PC formats), iosDdsxConv and
# andDdsxConv (the mobile formats of iOS and Android). jam built them rel only, so without a config suffix.
foreach(plugin pc ios and)
  set(defines)
  if(plugin STREQUAL "ios")
    set(defines IOS_EXP BUILD_FOR_MOBILE_TEXFMT)
  elseif(plugin STREQUAL "and")
    set(defines TEGRA_EXP BUILD_FOR_MOBILE_TEXFMT)
  endif()
  dagor_add_library(${plugin}DdsxConv SHARED LAX OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin/plugins/ddsx NO_CONFIG_POSTFIX
    ddsxConvPc.cpp main_mem.cpp)
  target_include_directories(${plugin}DdsxConv PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/tools/sharedInclude)
  target_compile_definitions(${plugin}DdsxConv PRIVATE ${defines})
  dagor_install_cdk(${plugin}DdsxConv SUBDIR plugins/ddsx)
endforeach()
