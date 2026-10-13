# VR device interface: a stub in the programs without VR. The programs with VR set the DAGOR_VR target property and
# get engine.drv.vr_device.vr: the OpenXR device on Windows and Android, the null device elsewhere, and the emulator in
# Dev and Dbg; see dagor_add_link_choice().
set(device engine.drv.vr_device.nullVrDevice)
if(WIN32 OR ANDROID)
  set(device engine.drv.vr_device.openXr)
endif()
dagor_add_target(NAME engine.drv.vr_device.vr STATIC LAX
  FILES_CMAKE vr_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${device}
    "$<IF:$<CONFIG:Dev,Dbg>,engine.drv.vr_device.emulator,engine.drv.vr_device.emulator.stub>"
)
dagor_add_target(NAME engine.drv.vr_device.stub STATIC LAX
  FILES_CMAKE stub_files.cmake
)
dagor_add_link_choice(engine.drv.vr_device PROPERTY DAGOR_VR ON engine.drv.vr_device.vr OFF engine.drv.vr_device.stub)
