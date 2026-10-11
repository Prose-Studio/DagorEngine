# Joysticks and gamepads on macOS (IOKit HID)
dagor_add_library(
  SOURCES joy_create.cpp joy_classdrv.cpp joy_device.cpp joy_composite.cpp osx_hid_util.cpp
  # IOHIDManagerRegisterDeviceMatchingCallback and IOHIDManagerRegisterDeviceRemovalCallback
  COMPILE_OPTIONS -Wno-nonnull
)
