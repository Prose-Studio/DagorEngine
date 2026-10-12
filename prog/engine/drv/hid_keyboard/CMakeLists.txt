if(LINUX)
  set(libs System::X11)
endif()

dagor_add_target(NAME engine.drv.hid_keyboard STATIC LAX
  FILES_CMAKE hid_keyboard_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PUBLIC ${libs}
)
