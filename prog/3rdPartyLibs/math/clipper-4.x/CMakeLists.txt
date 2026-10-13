if("${DAGOR_PLATFORM}-${DAGOR_ARCH}" STREQUAL "windows-x86_64")
  list(APPEND options /wd4267)
endif()

dagor_add_target(NAME 3rdPartyLibs.math.clipper-4.x STATIC LAX
  FILES_CMAKE clipper-4.x_files.cmake
  COMPILE_DEFINITIONS PRIVATE NEED_LL_ABS
  COMPILE_OPTIONS PRIVATE ${options}
)
