set(sources bsdiff.c bspatch.c)
list(APPEND force_includes supp/dag_null.h)

dagor_add_library(3rdPartyLibs.bsdiff LAX ${sources})
dagor_target_force_include(3rdPartyLibs.bsdiff ${force_includes})
