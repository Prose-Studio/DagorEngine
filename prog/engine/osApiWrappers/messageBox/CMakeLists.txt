# os_message_box(): the system's message box (FLTK on Linux)
set(sources)
set(libs)
set(options)
set(includes)
if(DAGOR_PLATFORM STREQUAL "windows")
  set(sources messageBox.cpp)
  set(libs Comctl32)
elseif(DAGOR_PLATFORM STREQUAL "macOS")
  set(sources macMessageBox.mm macOsMessageBox.cpp)
  set(options -Wno-error)
elseif(DAGOR_PLATFORM STREQUAL "linux")
  set(sources linuxMessageBox.cpp)
  set(libs X11 fltk)
  if(IS_DIRECTORY /usr/include/cairo)
    set(includes /usr/include/cairo) # the system FLTK's headers include cairo's
  endif()
elseif(DAGOR_PLATFORM STREQUAL "android")
  set(sources and_MessageBox.cpp) # TODO(phase5): MessageBoxWrapper.java and android_mb.proguard go into the APK
elseif(DAGOR_PLATFORM MATCHES "^(iOS|tvOS)$")
  set(sources iosMessageBox.mm)
endif()

dagor_add_library(STRICT
  SOURCES ${sources}
  PRIVATE_INCLUDES ${DAGOR_PROG_DIR}/engine/sharedInclude ${includes}
  PRIVATE_DEFINES __B_KERNEL_LIB __B_NO_MEM_BASE_INCLUDE
  COMPILE_OPTIONS ${options}
  SYSTEM_LIBS ${libs}
)
