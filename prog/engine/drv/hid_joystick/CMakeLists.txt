set(sources
  joy_classdrv.cpp
  joy_device.cpp
  joy_ff_effects.cpp
  joy_enumdev.cpp
  joy_create.cpp
  joy_composite.cpp
)
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)

dagor_add_library(engine.drv.hid_joystick LAX ${sources})
target_include_directories(engine.drv.hid_joystick PRIVATE ${includes})
