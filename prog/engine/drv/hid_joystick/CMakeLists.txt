dagor_add_target(NAME engine.drv.hid_joystick STATIC LAX
  FILES_CMAKE hid_joystick_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
)
