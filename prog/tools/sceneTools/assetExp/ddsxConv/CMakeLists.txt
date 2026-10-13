# The DDSx texture converter plugins of daBuild and the tools (plugins/ddsx): pcDdsxConv (PC formats), iosDdsxConv and
# andDdsxConv (the mobile formats of iOS and Android). Always optimized, so without a config suffix.
foreach(plugin pc ios and)
  set(defines)
  if(plugin STREQUAL "ios")
    set(defines IOS_EXP BUILD_FOR_MOBILE_TEXFMT)
  elseif(plugin STREQUAL "and")
    set(defines TEGRA_EXP BUILD_FOR_MOBILE_TEXFMT)
  endif()
  dagor_add_target(NAME ${plugin}DdsxConv SHARED LAX NO_CONFIG_POSTFIX
    OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin/plugins/ddsx
    FILES_CMAKE ddsxConv_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
    COMPILE_DEFINITIONS PRIVATE ${defines}
    CDK_SUBDIR plugins/ddsx
  )
endforeach()
