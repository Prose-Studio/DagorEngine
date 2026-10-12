set(FILES memtrace.cpp sqmem_dagor.cpp)
# no reuse of freed blocks under ASan, which then sees use after free
if(DAGOR_SANITIZE STREQUAL "address")
  set_property(SOURCE sqmem_dagor.cpp APPEND PROPERTY COMPILE_OPTIONS -DENABLE_RE_USE=0)
endif()
