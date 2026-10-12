# Google's cpu_features: the CPU's vendor, model and instruction set extensions, per platform and architecture
set(c_options -DSTACK_LINE_READER_BUFFER_SIZE=1024)
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin)$")
  if(DAGOR_ARCH STREQUAL "arm64")
    list(APPEND c_options -DHAVE_DLFCN_H)
  else()
    list(APPEND c_options -DHAVE_SYSCTLBYNAME)
  endif()
elseif(LINUX)
elseif(WIN32)
else()
  message(FATAL_ERROR "3rdPartyLibs/cpu_features does not support ${DAGOR_PLATFORM}")
endif()
if(APPLE AND DAGOR_ARCH STREQUAL "arm64")
  list(APPEND c_options -DHAVE_SYSCTLBYNAME)
endif()

dagor_add_target(NAME 3rdPartyLibs.cpu_features STATIC LAX
  FILES_CMAKE cpu_features_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include include/internal
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
