# Joysticks and gamepads on Linux (udev, XInput-like gamepads)
dagor_add_target(NAME engine.drv.hid_joystick_linux STATIC LAX
  FILES_CMAKE hid_joystick_linux_files.cmake
)
