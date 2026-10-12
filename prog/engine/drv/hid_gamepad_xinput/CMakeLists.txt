set(sources gamepad_classdrv.cpp gamepad_device.cpp gamepad_create.cpp mouse_emu.cpp)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  set(deps engine.baseUtil)
endif()
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)

dagor_add_library(engine.drv.hid_gamepad_xinput LAX ${sources})
target_include_directories(engine.drv.hid_gamepad_xinput PRIVATE ${includes})
target_link_libraries(engine.drv.hid_gamepad_xinput PRIVATE ${deps})
