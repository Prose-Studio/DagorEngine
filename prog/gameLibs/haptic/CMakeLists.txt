if(ANDROID)
  set(AndroidSources android/android.bundle/src/DagorHaptic.java)
endif()

dagor_add_target(NAME gameLibs.haptic STATIC LAX
  FILES_CMAKE haptic_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude/haptic
)
