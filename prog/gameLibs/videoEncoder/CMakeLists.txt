if(WIN32)
  list(APPEND libs System::mfuuid System::winmm)
endif()

dagor_add_target(NAME gameLibs.videoEncoder STATIC LAX
  FILES_CMAKE videoEncoder_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode
  BUILD_DEPENDENCIES PUBLIC ${libs}
)
