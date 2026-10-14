# what each build of daScript (standard, console) compiles itself: the sources that read DAS_DEFAULT_STDOUT or
# DAS_USE_BASE_CRASH_HANDLER; daScript_files.cmake has the rest, which both builds share
set(FILES src/misc/string_writer.cpp src/runtime/context.cpp src/misc/gc_node.cpp src/hal/crash_handler.cpp)
list(TRANSFORM FILES PREPEND "${CMAKE_CURRENT_LIST_DIR}/")
