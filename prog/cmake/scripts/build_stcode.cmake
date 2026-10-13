# cmake -DSOURCE_DIR=<dir> -DBINARY_DIR=<dir> -DPLATFORM=<platform> -DARCH=<arch> -DCONFIG=<Dev|Rel|Dbg> -DNAME=<name>
#       -DOUTPUT_DIR=<dir> [-DCLEAN=ON] -P build_stcode.cmake
# Builds the shaders' state code as C++ (the shader compilers' -cppStcode): the library of the CMakeLists.txt they write
# into SOURCE_DIR (from prog/tools/ShaderCompiler2/_stcodeTemplates/CMakeLists.txt.fmt), for PLATFORM (windows, linux,
# macOS, iOS, android) and ARCH (DAGOR_ARCH: x86_64, arm64, universal, e2k) with the engine's toolchain of the platform,
# into OUTPUT_DIR as <NAME>[-dev|-dbg]. CLEAN rebuilds everything (the generated code's format changed).
cmake_minimum_required(VERSION 4.0)
foreach(var SOURCE_DIR BINARY_DIR PLATFORM ARCH CONFIG NAME OUTPUT_DIR)
  if(NOT DEFINED ${var} OR "${${var}}" STREQUAL "")
    message(FATAL_ERROR "build_stcode.cmake: -D${var}=... is required")
  endif()
endforeach()
set(toolchain_windows windows-clang)
set(toolchain_linux linux-gcc)
set(toolchain_macOS macos)
set(toolchain_iOS ios)
set(toolchain_android android)
if(NOT DEFINED toolchain_${PLATFORM})
  message(FATAL_ERROR "build_stcode.cmake: the state code of platform ${PLATFORM} can't be built here")
endif()
if(NOT CONFIG MATCHES "^(Dev|Rel|Dbg)$")
  message(FATAL_ERROR "build_stcode.cmake: CONFIG is Dev, Rel or Dbg, not ${CONFIG}")
endif()
cmake_path(GET CMAKE_CURRENT_LIST_DIR PARENT_PATH cmake_dir) # prog/cmake
foreach(var SOURCE_DIR BINARY_DIR OUTPUT_DIR)
  cmake_path(ABSOLUTE_PATH ${var} NORMALIZE)
endforeach()

execute_process(
  COMMAND "${CMAKE_COMMAND}" -S "${SOURCE_DIR}" -B "${BINARY_DIR}" -G "Ninja Multi-Config"
    "-DCMAKE_TOOLCHAIN_FILE=${cmake_dir}/toolchains/${toolchain_${PLATFORM}}.cmake" "-DDAGOR_ARCH=${ARCH}"
    "-DDagor_DIR=${cmake_dir}" "-DDAGOR_STCODE_NAME=${NAME}" "-DDAGOR_STCODE_OUTPUT_DIRECTORY=${OUTPUT_DIR}"
  RESULT_VARIABLE result)
if(result)
  message(FATAL_ERROR "build_stcode.cmake: configuring ${SOURCE_DIR} failed")
endif()
set(clean)
if(CLEAN)
  set(clean --clean-first)
endif()
execute_process(COMMAND "${CMAKE_COMMAND}" --build "${BINARY_DIR}" --config ${CONFIG} ${clean} RESULT_VARIABLE result)
if(result)
  message(FATAL_ERROR "build_stcode.cmake: building ${SOURCE_DIR} failed")
endif()
