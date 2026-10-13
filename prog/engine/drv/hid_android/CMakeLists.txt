# Android input (touch, gamepads, the soft keyboard)
# TODO(android): NvSoftInput.java, GamepadHelper.java and and.proguard go into the APK
dagor_add_target(NAME engine.drv.hid_android STATIC LAX
  FILES_CMAKE hid_android_files.cmake
)
