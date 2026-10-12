# Intel's ISPC Texture Compressor (BC1-7, ETC1, ASTC) with its ISPC kernels for several instruction sets (the best one
# is picked at run time); GameTechDev/ISPCTextureCompressor rev 691513b4. The kernels are compiled by the ISPC SDK
# (fetched when a tree builds this library) into the build dir, with the <kernel>_ispc.h headers the sources include
# (CMake's ISPC language names them after the objects, which its SHORT intermediate dirs hash).
if(DAGOR_ARCH STREQUAL "x86_64")
  set(targets sse2-i32x4,sse4-i32x4,avx1-i32x8,avx2-i32x8)
  set(isa_suffixes sse2 sse4 avx avx2)
  set(ispc_arch x86-64)
elseif(DAGOR_ARCH STREQUAL "arm64")
  set(targets neon-i32x4)
  set(isa_suffixes)
  set(ispc_arch aarch64)
else()
  message(FATAL_ERROR "3rdPartyLibs/convert/ispc_texcomp has no ISPC targets for ${DAGOR_ARCH}")
endif()
dagor_fetch_sdk(ispc ispc_dir)
find_program(DAGOR_ISPC NAMES ispc PATHS "${ispc_dir}/bin" NO_DEFAULT_PATH REQUIRED)
set(os windows)
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(os macos)
elseif(LINUX)
  set(os linux)
endif()
set(obj_ext .o)
if(WIN32)
  set(obj_ext .obj)
endif()

set(gen "${CMAKE_CURRENT_BINARY_DIR}/gen")
set(objects)
set(headers)
foreach(kernel kernel kernel_astc)
  # one object per instruction set (<kernel>_<isa>), and the dispatcher (<kernel>) when there are several
  set(outputs "${gen}/${kernel}${obj_ext}")
  foreach(suffix IN LISTS isa_suffixes)
    list(APPEND outputs "${gen}/${kernel}_${suffix}${obj_ext}")
  endforeach()
  add_custom_command(OUTPUT ${outputs} "${gen}/${kernel}_ispc.h"
    COMMAND "${DAGOR_ISPC}" "${CMAKE_CURRENT_SOURCE_DIR}/${kernel}.ispc" -O2 --pic --opt=fast-math --woff
      --arch=${ispc_arch} --target=${targets} --target-os=${os} -o "${gen}/${kernel}${obj_ext}"
      -h "${gen}/${kernel}_ispc.h"
    DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/${kernel}.ispc" "${DAGOR_ISPC}"
    COMMENT "ISPC ${kernel}.ispc (${targets})"
    VERBATIM)
  list(APPEND objects ${outputs})
  list(APPEND headers "${gen}/${kernel}_ispc.h")
endforeach()
file(MAKE_DIRECTORY "${gen}")
set_source_files_properties(${objects} PROPERTIES EXTERNAL_OBJECT ON GENERATED ON)

dagor_add_library(3rdPartyLibs.convert.ispc_texcomp LAX ispc_texcomp.cpp ispc_texcomp_astc.cpp ${objects} ${headers})
target_include_directories(3rdPartyLibs.convert.ispc_texcomp PRIVATE "${gen}")
dagor_target_licenses(3rdPartyLibs.convert.ispc_texcomp license.txt)
