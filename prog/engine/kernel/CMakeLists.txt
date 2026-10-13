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
  list(APPEND includes ${DAGOR_ANDROID_NDK}/sources/android/cpufeatures)
endif()
if(DAGOR_BREAKPAD)
  list(APPEND defines __BREAKPAD_ENABLED)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad)
  list(APPEND deps 3rdPartyLibs.breakpad)
endif()

dagor_add_target(NAME engine.kernel STATIC
  FILES_CMAKE kernel_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
