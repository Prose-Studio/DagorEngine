set(FILES src/alloc.c src/alloc-aligned.c src/alloc-posix.c src/arena.c src/bitmap.c src/heap.c src/init.c
  src/libc.c src/options.c src/os.c src/page.c src/random.c src/segment.c src/segment-map.c src/stats.c)
if(WIN32)
  list(APPEND FILES src/prim/windows/prim.c)
else()
  list(APPEND FILES src/prim/unix/prim.c)
endif()
