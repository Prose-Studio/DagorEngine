# The Linux GUI layer (window title, clipboard, event loop) on X11 and Wayland, for programs with DAGOR_LINUX_GUI
if(NOT LINUX)
  return()
endif()
if(NOT DAGOR_LINUX_X11 AND NOT DAGOR_LINUX_WAYLAND)
  message(FATAL_ERROR "DAGOR_LINUX_X11 or DAGOR_LINUX_WAYLAND must be on")
endif()
set(defines)
set(deps)
set(libs System::xkbcommon)
if(DAGOR_LINUX_WAYLAND)
  list(APPEND defines USE_WAYLAND)
  list(APPEND deps 3rdPartyLibs.wayland)
endif()
if(DAGOR_LINUX_X11)
  list(APPEND defines USE_X11)
  list(APPEND libs System::X11 System::Xcursor)
  # XInput2's header (raw mouse motion; libXi itself is loaded at run time, when there)
  find_path(DAGOR_XINPUT2_INCLUDE_DIR X11/extensions/XInput2.h)
  if(NOT DAGOR_XINPUT2_INCLUDE_DIR)
    message(FATAL_ERROR "X11/extensions/XInput2.h not found: install libXi's development package (libxi-dev, "
      "libXi-devel)")
  endif()
endif()

dagor_add_target(NAME engine.osApiWrappers.linuxGUI STATIC
  FILES_CMAKE linuxGUI_files.cmake
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
)
