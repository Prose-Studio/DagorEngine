set(FILES vars.cpp events.cpp streams.cpp banks.cpp attributes.cpp delayed.cpp releasing.cpp update.cpp mixing.cpp
  soundSystem.cpp dagorFmodStudioAudioSys.cpp dsp.cpp nullAudio.cpp userCreatedSound.cpp eventInstanceStealing.cpp
  visualLabels.cpp occlusion.cpp occlusionGPU.cpp assertsMonitor.cpp stub/steamAudioStub.cpp
  $<IF:$<CONFIG:Rel>,stub/debugStub.cpp,debug.cpp>)
