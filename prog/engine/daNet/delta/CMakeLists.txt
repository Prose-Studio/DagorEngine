# daNet delta compression (RLE, history buffers)
add_subdirectory(tests)

set(sources rle.cpp history.cpp buffer.cpp deltaCompression.cpp)
list(APPEND deps engine.daNet)

dagor_add_library(engine.daNet.delta ${sources})
target_link_libraries(engine.daNet.delta PRIVATE ${deps})
