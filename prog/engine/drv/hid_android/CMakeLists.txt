# Android input (touch, gamepads, the soft keyboard), with the Java classes it calls in the apps' APKs
dagor_add_target(NAME engine.drv.hid_android STATIC LAX
  FILES_CMAKE hid_android_files.cmake
)
dagor_target_android_java(engine.drv.hid_android NvSoftInput.java GamepadHelper.java)
