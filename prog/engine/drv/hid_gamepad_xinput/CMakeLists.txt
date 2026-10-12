if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  set(deps engine.baseUtil)
endif()

dagor_add_target(NAME engine.drv.hid_gamepad_xinput STATIC LAX
  FILES_CMAKE hid_gamepad_xinput_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
