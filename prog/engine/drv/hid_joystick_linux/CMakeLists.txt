# Joysticks and gamepads on Linux (udev, XInput-like gamepads)
dagor_add_library(engine.drv.hid_joystick_linux LAX joy_composite.cpp hid_udev.cpp joy_create.cpp joy_classdrv.cpp
  joy_device.cpp joy_device_xinput.cpp)
