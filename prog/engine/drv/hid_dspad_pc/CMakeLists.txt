# DualShock and DualSense pads on PCs (HID on Windows and Linux, Steam's input), with their touchpad gestures
if(NOT WIN32 AND NOT LINUX)
  message(FATAL_ERROR "engine/drv/hid_dspad_pc: no ${DAGOR_PLATFORM} support")
endif()
dagor_add_target(NAME engine.drv.hid_dspad_pc STATIC LAX
  FILES_CMAKE hid_dspad_pc_files.cmake
)
