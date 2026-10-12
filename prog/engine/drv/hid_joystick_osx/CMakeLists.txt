# Joysticks and gamepads on macOS (IOKit HID)
# IOHIDManagerRegisterDeviceMatchingCallback and IOHIDManagerRegisterDeviceRemovalCallback
dagor_add_target(NAME engine.drv.hid_joystick_osx STATIC LAX
  FILES_CMAKE hid_joystick_osx_files.cmake
  COMPILE_OPTIONS PRIVATE -Wno-nonnull
)
