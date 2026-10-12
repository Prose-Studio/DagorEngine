set(FILES src/base/ftmac.c)
set_property(SOURCE src/bdf/bdflib.c APPEND PROPERTY COMPILE_OPTIONS -Wno-deprecated-declarations)
