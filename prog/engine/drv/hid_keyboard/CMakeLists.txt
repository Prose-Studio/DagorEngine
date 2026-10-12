set(sources kbd_shifts.cpp kbd_device_common.cpp kbd_globals.cpp kbd_classdrv_win.cpp kbd_device_win.cpp)
if(LINUX)
  set(libs System::X11)
endif()
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)

dagor_add_library(engine.drv.hid_keyboard LAX ${sources})
target_include_directories(engine.drv.hid_keyboard PRIVATE ${includes})
target_link_libraries(engine.drv.hid_keyboard PUBLIC ${libs})
