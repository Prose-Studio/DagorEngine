# (DAGOR_LINUX_GUI)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.linuxGUI)
endif()

dagor_add_target(NAME engine.drv.hid_mouse STATIC LAX
  FILES_CMAKE hid_mouse_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
