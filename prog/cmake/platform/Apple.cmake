# What macOS and iOS share (included by Darwin.cmake and iOS.cmake).
dagor_compile_definitions(1 _TARGET_64BIT)
dagor_compile_definitions("${_dbg}" DAS_FUSION=0)
dagor_link_options("${_linked}" -ObjC LINKER:-headerpad_max_install_names)
# programs load the dynamic libraries next to them (daKernel, an SDK's runtime files), built and installed
set(CMAKE_BUILD_RPATH "@executable_path")
set(CMAKE_INSTALL_RPATH "@executable_path")
if(CMAKE_GENERATOR STREQUAL "Xcode")
  # Xcode's default build settings add warnings of their own; the one clang does not enable anyway is turned off, so
  # the project builds as it does with Ninja
  set(CMAKE_XCODE_ATTRIBUTE_GCC_WARN_64_TO_32_BIT_CONVERSION NO)
endif()
