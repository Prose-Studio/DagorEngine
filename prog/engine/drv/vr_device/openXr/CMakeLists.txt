# The OpenXR VR device (Windows, Android) on the Khronos OpenXR loader, with its input; a program without an OpenXR
# runtime or headset starts without VR instead of asserting (SILENT_VRDEVICE_FAIL)
find_package(OpenXR REQUIRED)
dagor_add_target(NAME engine.drv.vr_device.openXr STATIC LAX
  FILES_CMAKE openXr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include
  COMPILE_DEFINITIONS PRIVATE SILENT_VRDEVICE_FAIL
  BUILD_DEPENDENCIES PRIVATE OpenXR::OpenXR
)
