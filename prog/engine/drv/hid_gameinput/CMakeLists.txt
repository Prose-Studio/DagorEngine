if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  set(deps engine.baseUtil)
endif()

dagor_add_target(NAME engine.drv.hid_gameinput STATIC LAX
  FILES_CMAKE hid_gameinput_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
