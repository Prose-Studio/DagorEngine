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
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND FILES gamelib/soundMac.mm)
else()
  list(APPEND FILES gamelib/sound.cpp)
endif()
if(NOT WIN32 AND NOT LINUX AND NOT DAGOR_PLATFORM STREQUAL
  "android" AND IOS)
  list(APPEND FILES platform/ios_main.mm)
  # TODO(jam): BundleID = com.gaijinent.dargbox ;
  # TODO(jam): BundleName = dargbox ;
  # TODO(jam): BundlePlist = @$(Root)/prog/_jBuild/iOS/generic.info.plist ../Info.plist ;
  # TODO(jam): BundleCopy =  ;
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND FILES platform/macosx_main.mm)
  # TODO(jam): Exit unsupported Platform\=$(Platform) for Target\=$(Target) ;
endif()
