# Joysticks and gamepads on macOS (IOKit HID)
# IOHIDManagerRegisterDeviceMatchingCallback and IOHIDManagerRegisterDeviceRemovalCallback
dagor_add_library(engine.drv.hid_joystick_osx LAX joy_create.cpp joy_classdrv.cpp joy_device.cpp joy_composite.cpp
  osx_hid_util.cpp # IOHIDManagerRegisterDeviceMatchingCallback and IOHIDManagerRegisterDeviceRemovalCallback
)
target_compile_options(engine.drv.hid_joystick_osx PRIVATE -Wno-nonnull)
