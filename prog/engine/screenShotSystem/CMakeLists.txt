set(sources screenShotSystem.cpp)
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)

dagor_add_library(engine.screenShotSystem ${sources})
target_include_directories(engine.screenShotSystem PRIVATE ${includes})
