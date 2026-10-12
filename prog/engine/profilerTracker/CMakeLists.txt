# Profiler tracker API (a stub: the tracker itself is not part of the engine)
dagor_add_library(engine.profilerTracker LAX profilerTrackerStub.cpp)
target_include_directories(engine.profilerTracker PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude .)
