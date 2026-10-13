# os_message_box(): the system's message box (FLTK on Linux)
set(libs)
set(options)
if(WIN32)
  set(libs System::comctl32)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(options -Wno-error)
elseif(LINUX)
  find_package(FLTK REQUIRED)
  set(libs FLTK::FLTK)
endif()

dagor_add_target(NAME engine.osApiWrappers.messageBox STATIC
  FILES_CMAKE messageBox_files.cmake
  COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB __B_NO_MEM_BASE_INCLUDE
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PUBLIC ${libs}
)
