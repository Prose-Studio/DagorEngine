set(FILES
  app.cpp
  main.cpp
  joystick.cpp
  scriptBindings.cpp
  initScript.cpp
  vr.cpp
  vrInput.cpp
  gamelib/input.cpp
)
if(APPLE)
  list(APPEND FILES gamelib/soundMac.mm)
else()
  list(APPEND FILES gamelib/sound.cpp)
endif()
