# daECS utilities: entity helpers, templates DB, events
set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/eastl/include)
set(sources createInstantiated.cpp instantiateDependencies.cpp enumDescription.cpp)
list(APPEND deps engine.daECS.core)

dagor_add_library(engine.daECS.utility ${sources})
target_include_directories(engine.daECS.utility PRIVATE ${includes})
target_link_libraries(engine.daECS.utility PRIVATE ${deps})
