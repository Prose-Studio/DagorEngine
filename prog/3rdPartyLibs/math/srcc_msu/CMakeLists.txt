# is01r spline smoothing, a numerical routine translated from Fortran with f2c (origin unknown, see NO_LICENSE)
set(sources is01r_c.c)
list(APPEND force_includes supp/dag_null.h)

dagor_add_library(3rdPartyLibs.math.srcc_msu LAX ${sources})
dagor_target_force_include(3rdPartyLibs.math.srcc_msu ${force_includes})
