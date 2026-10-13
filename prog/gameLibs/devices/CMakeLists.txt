# Game devices on Windows (the other platforms link gameLibs/devices/stub): telemetry export; TrackIR head tracking and
# the jet seat as their stubs (UseHeadTracking and UseJetSeat are off in every game)
dagor_add_target(NAME gameLibs.devices STATIC LAX
  FILES_CMAKE devices_files.cmake
)
