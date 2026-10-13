# Fatal errors, logging, debug dumps, CPU frequency and hardware exception handling
set(not_rel "$<NOT:$<CONFIG:Rel>>")
set(includes)
set(deps)
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND includes "$<${not_rel}:${DAGOR_PROG_DIR}/3rdPartyLibs/minhook/Include>")
  list(APPEND deps "$<${not_rel}:3rdPartyLibs.minhook>")
endif()

set(defines __B_KERNEL_LIB __B_NO_MEM_BASE_INCLUDE)
if(NOT DAGOR_SANITIZE STREQUAL "none" AND CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
  list(APPEND defines DAGOR_CAPTURE_STDERR) # the sanitizers write to stderr; this disables asynchronous log writes
endif()
if(ANDROID)
  list(APPEND defines ANDROID_ENABLE_SIGNAL_LOG) # the log of a fatal signal's stack (dagorHwExcept.cpp)
  list(APPEND includes ${DAGOR_ANDROID_NDK}/sources/android/cpufeatures)
endif()
list(APPEND defines "$<${DAGOR_BREAKPAD_CONFIGS}:__BREAKPAD_ENABLED>")
list(APPEND includes "$<${DAGOR_BREAKPAD_CONFIGS}:${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad>")
list(APPEND deps "$<${DAGOR_BREAKPAD_CONFIGS}:3rdPartyLibs.breakpad>")

dagor_add_target(NAME engine.kernel STATIC
  FILES_CMAKE kernel_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
