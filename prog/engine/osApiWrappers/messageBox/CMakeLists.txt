# os_message_box(): the system's message box (FLTK on Linux)
add_subdirectory(stub)
set(libs)
set(options)
set(includes)
if(WIN32)
  set(libs System::comctl32)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(options -Wno-error)
elseif(LINUX)
  set(libs System::X11 System::fltk)
  if(IS_DIRECTORY /usr/include/cairo)
    set(includes /usr/include/cairo) # the system FLTK's headers include cairo's
  endif()
endif()

dagor_add_target(NAME engine.osApiWrappers.messageBox STATIC
  FILES_CMAKE messageBox_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${includes}
  COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB __B_NO_MEM_BASE_INCLUDE
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PUBLIC ${libs}
)
