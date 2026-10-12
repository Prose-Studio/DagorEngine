set(sources
  kbd_null.cpp
  kbd_null_gen.cpp
  ms_null.cpp
  ms_null_gen.cpp
  joy_null.cpp
  joy_null_gen.cpp
  joy_null_xinp.cpp
  joy_null_comp.cpp
  dx_null.cpp
)

dagor_add_library(engine.drv.hid_nulldrv LAX ${sources})
