# The compile and link settings of every target in the tree: directory properties of the top-level directory
# (add_compile_options, add_compile_definitions, add_link_options, link_libraries), which the targets below it start
# with, so a target's own options come after them. The toolchain's flag overrides drop CMake's defaults
# (toolchains/flag-overrides.cmake): what is here is the whole command line apart from the toolchain's paths.
#
# Per-target choices are target properties the settings read through generator expressions:
#   DAGOR_EXCEPTIONS  ON, OFF or SEH (also structured exceptions); unset: the tree's DAGOR_EXCEPTIONS_CONFIGS
#   DAGOR_RTTI        ON or OFF; unset: DAGOR_RTTI
#   DAGOR_FRAME_LIMIT the stack frame limit of strict code in bytes (clang-cl; 32768 by default)
# The warnings of first-party and third-party code are the lists DAGOR_STRICT_OPTIONS and DAGOR_LAX_OPTIONS, which
# dagor_add_target() adds to each target (LAX picks the second).
include_guard(GLOBAL)

set(CMAKE_CXX_STANDARD ${DAGOR_CPP_STD})
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_SCAN_FOR_MODULES OFF) # the engine has no C++20 modules
# a static or object library does not wait for the libraries it links (only for those with generated sources or custom
# commands): they build in parallel, and a library of a choice (dagor_add_link_choice) is built only for the programs
# that link it
set(CMAKE_OPTIMIZE_DEPENDENCIES ON)
if(NOT MSVC)
  set(CMAKE_C_STANDARD 99)
  set(CMAKE_C_EXTENSIONS OFF)
endif()
# the static CRT; the 3ds Max plugins the DLL one, as Max loads them
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Dbg>:Debug>")
if(DAGOR_VARIANT STREQUAL "maxplug")
  set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Dbg>:Debug>DLL")
endif()
if(NOT CMAKE_MSVC_DEBUG_INFORMATION_FORMAT) # (with a compiler cache /Z7: toolchains/_common.cmake)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT ProgramDatabase)
endif()
set_property(GLOBAL PROPERTY DEBUG_CONFIGURATIONS Dbg)
foreach(_cfg DEV REL IREL)
  set(CMAKE_MAP_IMPORTED_CONFIG_${_cfg} Release RelWithDebInfo MinSizeRel "")
endforeach()
set(CMAKE_MAP_IMPORTED_CONFIG_DBG Debug "")
if(DAGOR_UNITY_BUILD)
  set(CMAKE_UNITY_BUILD ON)
endif()
if(NOT DAGOR_LTO STREQUAL "OFF")
  include(CheckIPOSupported)
  check_ipo_supported(RESULT _ipo OUTPUT _ipo_error LANGUAGES C CXX)
  if(NOT _ipo)
    message(FATAL_ERROR "DAGOR_LTO=${DAGOR_LTO}: the compiler has no link-time optimization: ${_ipo_error}")
  endif()
  set(CMAKE_INTERPROCEDURAL_OPTIMIZATION ON)
  unset(_ipo)
  unset(_ipo_error)
endif()

# conditions
set(_c_cxx "$<COMPILE_LANGUAGE:C,CXX,OBJC,OBJCXX>") # Objective-C(++) sources get the settings of C(++)
set(_cxx "$<COMPILE_LANGUAGE:CXX,OBJCXX>")
set(_dev "$<CONFIG:Dev>")
set(_rel "$<CONFIG:Rel>")
set(_dbg "$<CONFIG:Dbg>")
set(_release "$<CONFIG:Rel,IRel>")
set(_exe "$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>")
# (no list in a generator expression here: the commands taking these would split it at its semicolons)
set(_linked "$<OR:${_exe},$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>,$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>>")
# _dagor_configs(<out> <config>...): the condition of a list of configurations (0 for none)
function(_dagor_configs out)
  if(ARGN)
    list(JOIN ARGN "," joined)
    set(${out} "$<CONFIG:${joined}>" PARENT_SCOPE)
  else()
    set(${out} 0 PARENT_SCOPE)
  endif()
endfunction()
_dagor_configs(_checked ${DAGOR_CHECKED_CONTAINERS_CONFIGS})
_dagor_configs(_stack_protection ${DAGOR_STACK_PROTECTION_CONFIGS})
if(DAGOR_SANITIZE STREQUAL "address")
  set(_stack_protection 0)
endif()
_dagor_configs(_exceptions ${DAGOR_EXCEPTIONS_CONFIGS})
set(_exc_prop "$<TARGET_PROPERTY:DAGOR_EXCEPTIONS>")
set(_exceptions
  "$<IF:$<STREQUAL:${_exc_prop},>,${_exceptions},$<OR:$<STREQUAL:${_exc_prop},ON>,$<STREQUAL:${_exc_prop},SEH>>>")
if(DAGOR_CATCH_SEH)
  set(_seh "$<AND:${_exceptions},$<NOT:$<STREQUAL:${_exc_prop},ON>>>")
else()
  set(_seh "$<STREQUAL:${_exc_prop},SEH>")
endif()
set(_rtti_default 0)
if(DAGOR_RTTI)
  set(_rtti_default 1)
endif()
set(_rtti "$<IF:$<STREQUAL:$<TARGET_PROPERTY:DAGOR_RTTI>,>,${_rtti_default},$<STREQUAL:$<TARGET_PROPERTY:DAGOR_RTTI>,ON>>")
set(_cxx_exceptions "$<AND:${_cxx},${_exceptions}>")
set(_cxx_no_exceptions "$<AND:${_cxx},$<NOT:${_exceptions}>>")
set(_opt "$<AND:${_c_cxx},$<NOT:${_dbg}>>")
set(_unopt "$<AND:${_c_cxx},${_dbg}>")
set(_sp "$<AND:${_c_cxx},${_stack_protection}>")
set(_no_sp "$<AND:${_c_cxx},$<NOT:${_stack_protection}>>")

# dagor_compile_options(<condition> <option>...), dagor_compile_definitions(<condition> <definition>...),
# dagor_link_options(<condition> <option>...): tree settings under a condition (1: always). The definitions are not
# passed to the assemblers.
function(dagor_compile_options cond)
  foreach(value IN LISTS ARGN)
    if(cond STREQUAL "1")
      add_compile_options("${value}")
    else()
      add_compile_options("$<${cond}:${value}>")
    endif()
  endforeach()
endfunction()
function(dagor_compile_definitions cond)
  foreach(value IN LISTS ARGN)
    add_compile_definitions("$<$<AND:$<COMPILE_LANGUAGE:C,CXX,OBJC,OBJCXX,RC>,${cond}>:${value}>")
  endforeach()
endfunction()
function(dagor_link_options cond)
  foreach(value IN LISTS ARGN)
    add_link_options("$<${cond}:${value}>")
  endforeach()
endfunction()

# --- definitions ------------------------------------------------------------------------------------------------------
dagor_compile_definitions(1 "DAGOR_DBGLEVEL=$<IF:${_dbg},2,$<IF:${_dev},1,$<IF:${_rel},0,-1>>>")
dagor_compile_definitions("${_release}" NDEBUG)
dagor_compile_definitions("${_checked}" _DEBUG_TAB_ EASTL_DEBUG EASTL_DEBUGPARAMS_LEVEL=0 EASTL_NAME_ENABLED=0)
dagor_compile_definitions("${_cxx_exceptions}" DAGOR_EXCEPTIONS_ENABLED)
if(DAGOR_KERNEL_LINKAGE STREQUAL "static")
  dagor_compile_definitions(1 _TARGET_STATIC_LIB)
endif()
if(DAGOR_FORCE_LOGS)
  dagor_compile_definitions("${_release}" DAGOR_FORCE_LOGS)
endif()
if(DAGOR_D3D_MULTI)
  dagor_compile_definitions(1 _TARGET_D3D_MULTI)
endif()
if(NOT DAGOR_TIME_PROFILER)
  dagor_compile_definitions(1 TIME_PROFILER_ENABLED=0)
endif()
if(DAGOR_ARCH MATCHES "^(x86_64|e2k)$" AND NOT APPLE)
  dagor_compile_definitions(1 _TARGET_SIMD_SSE=${DAGOR_SSE})
endif()

# --- include dirs and the forced includes -----------------------------------------------------------------------------
# the base include dirs come before a target's own: headers like daScript/das_config.h resolve to the
# engine's (prog/1stPartyLibs/daScript) rather than to a library's include dir
include_directories(BEFORE
  "${DAGOR_PROG_DIR}/dagorInclude"
  "${DAGOR_PROG_DIR}/1stPartyLibs"
  "${DAGOR_PROG_DIR}/3rdPartyLibs"
  "$<${_cxx}:${DAGOR_PROG_DIR}/3rdPartyLibs/eastl/include>")
# the headers every C++ compile starts with (also for the code generators that parse the sources); the compatibility
# defines (__forceinline, ...) first: dag_memBase.h uses them
if(MSVC)
  set(DAGOR_FORCED_INCLUDES memory/dag_memBase.h)
  dagor_compile_options("${_cxx}" /FImemory/dag_memBase.h)
else()
  set(DAGOR_FORCED_INCLUDES supp/dag_compatibility_defines_posix.h memory/dag_memBase.h)
  dagor_compile_options("${_c_cxx}" "SHELL:-include supp/dag_compatibility_defines_posix.h")
  dagor_compile_options("${_cxx}" "SHELL:-include memory/dag_memBase.h")
endif()

# --- compiler flags ---------------------------------------------------------------------------------------------------
if(MSVC)
  dagor_compile_options("${_c_cxx}" /Zc:forScope /J /Zc:inline /Zc:wchar_t /FS /fp:${DAGOR_FP_MODEL})
  dagor_compile_options("${_unopt}" /Od /RTC1)
  dagor_compile_options("${_no_sp}" /GS-)
  dagor_compile_options("$<AND:${_cxx_exceptions},${_seh}>" /EHa)
  dagor_compile_options("$<AND:${_cxx_exceptions},$<NOT:${_seh}>>" /EHsc)
  dagor_compile_options("$<AND:${_cxx},$<NOT:${_rtti}>>" /GR-)
endif()

if(MSVC AND CMAKE_CXX_COMPILER_ID STREQUAL "Clang") # clang-cl
  dagor_compile_options("${_c_cxx}" /Zc:dllexportInlines- "SHELL:-Xclang -mrecip=none" -fms-extensions
    -fms-compatibility -fdiagnostics-absolute-paths -Wno-c++11-narrowing -Wno-trigraphs -Wno-argument-outside-range
    -Wno-nonportable-include-path -Wno-ignored-attributes -Wno-invalid-offsetof -Wno-multichar -Wno-unused-function
    -Wno-inconsistent-missing-override -Wno-invalid-token-paste -Wno-ignored-pragma-intrinsic -Wno-pragma-pack
    -Wno-microsoft -Wno-int-to-void-pointer-cast -Wno-expansion-to-defined -Wno-deprecated-declarations
    -Wno-constant-conversion -Wno-unused-local-typedef -Wno-ignored-pragmas -Wno-switch -Wno-deprecated-builtins
    -Wno-nontrivial-memcall -Werror=invalid-noreturn -Werror=return-type)
  dagor_compile_options("${_opt}" /clang:-O3 /Gy /Gw)
  if(DAGOR_FP_MODEL STREQUAL "fast")
    dagor_compile_options("${_c_cxx}" -Wno-nan-infinity-disabled)
  endif()
  if(DAGOR_ARCH STREQUAL "arm64")
    dagor_compile_options("${_c_cxx}" -Wno-pointer-to-int-cast)
  elseif(DAGOR_SSE EQUAL 4)
    dagor_compile_options("${_c_cxx}" -msse4.1 -mpopcnt -mcx16)
  else()
    dagor_compile_options("${_c_cxx}" -msse2)
  endif()
  if(DAGOR_STRICT_ALIASING)
    dagor_compile_options("${_c_cxx}" /clang:-fstrict-aliasing)
  endif()
elseif(MSVC) # cl
  # /X: only the toolchain's include dirs, never those of an INCLUDE environment variable (except under MSBuild, which
  # passes the toolset's and SDK's dirs that way)
  if(NOT CMAKE_GENERATOR MATCHES "^Visual Studio")
    dagor_compile_options("${_c_cxx}" /X)
  endif()
  dagor_compile_options("${_c_cxx}" /bigobj)
  dagor_compile_options("${_opt}" /Ox /GF /Gy /Gw /Oi /Ot /Oy-)
  if(DAGOR_ARCH STREQUAL "arm64")
    dagor_compile_options("${_c_cxx}" /wd4746)
  endif()
else() # gcc, clang and lcc
  dagor_compile_options("${_c_cxx}" -pipe -ffunction-sections -fdata-sections -Wno-trigraphs -Wno-multichar -Wformat)
  dagor_compile_options("${_opt}" -O3)
  dagor_compile_options("${_sp}" -fstack-protector)
  dagor_compile_options("${_no_sp}" -fno-stack-protector)
  dagor_compile_options("${_cxx}" -Wno-invalid-offsetof)
  dagor_compile_options("${_cxx_exceptions}" -fexceptions)
  dagor_compile_options("${_cxx_no_exceptions}" -fno-exceptions)
  # C++ only: Objective-C++ keeps the compiler's default RTTI (the Metal driver's dynamic_casts)
  dagor_compile_options("$<AND:$<COMPILE_LANGUAGE:CXX>,${_rtti}>" -frtti)
  dagor_compile_options("$<AND:$<COMPILE_LANGUAGE:CXX>,$<NOT:${_rtti}>>" -fno-rtti)
  if(DAGOR_FP_MODEL STREQUAL "fast")
    dagor_compile_options("${_c_cxx}" -ffast-math -ffinite-math-only)
    if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
      dagor_compile_options("${_c_cxx}" -mrecip=none -Wno-nan-infinity-disabled)
    elseif(DAGOR_ARCH STREQUAL "x86_64")
      dagor_compile_options("${_c_cxx}" -mno-recip)
    endif()
  endif()
  if(NOT DAGOR_STRICT_ALIASING)
    dagor_compile_options("${_c_cxx}" -fno-strict-aliasing)
  endif()
  if(DAGOR_MARCH)
    dagor_compile_options("${_c_cxx}" -march=${DAGOR_MARCH})
  endif()
  if(LINUX OR ANDROID)
    if(DAGOR_ARCH STREQUAL "x86_64")
      dagor_compile_options("${_c_cxx}" -msse${DAGOR_SSE} -minline-all-stringops)
    endif()
    dagor_compile_options("${_c_cxx}" -fno-omit-frame-pointer -Wuninitialized)
    dagor_compile_options("${_cxx}" -fvisibility-inlines-hidden)
    if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
      dagor_compile_options("${_opt}" -g)
      dagor_compile_options("${_unopt}" -ggdb3)
    else()
      dagor_compile_options("${_c_cxx}" -g)
    endif()
  else()
    dagor_compile_options("${_c_cxx}" -g)
  endif()

  if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    dagor_compile_options("${_c_cxx}" -Wno-format-extra-args -Wno-ignored-attributes -Wno-deprecated
      -Wno-format-truncation -Wno-nonnull -Werror=uninitialized -Wno-deprecated-declarations -Wno-maybe-uninitialized
      -Wno-stringop-overflow -Wno-stringop-overread)
  elseif(CMAKE_CXX_COMPILER_ID STREQUAL "LCC")
    dagor_compile_options("${_c_cxx}" -w2620 -w2189 -w826 -Wno-unused-parameter)
  elseif(APPLE)
    dagor_compile_options("$<COMPILE_LANGUAGE:OBJC,OBJCXX>" -fno-objc-exceptions)
    dagor_compile_options("$<COMPILE_LANGUAGE:OBJCXX>" -Wno-c99-designator -Wno-deprecated-enum-enum-conversion)
    if(IOS)
      # warnings are not errors on iOS, whose code still logs through the deprecated asl(3)
      dagor_compile_options("${_c_cxx}" -Wno-dangling-else -Wno-dynamic-class-memaccess -Wno-switch
        -Wno-constant-logical-operand -Wno-string-plus-int -Wno-unknown-warning-option -Wno-deprecated-register
        -Wno-deprecated-declarations -Wno-inconsistent-missing-override -Wno-null-dereference -Wno-constant-conversion
        -Wno-unused-value -Wno-deprecated-builtins -Wno-unused-command-line-argument -Wno-nontrivial-memcall)
    else()
      # the macOS builds have always been warning-free
      set(CMAKE_COMPILE_WARNING_AS_ERROR ON)
      dagor_compile_options("${_c_cxx}" -Wno-unused-value -Wno-uninitialized -Wno-inline-new-delete
        -Wno-unknown-warning-option -Wno-deprecated-register -Wno-nonportable-include-path -Wno-null-dereference
        -Wno-undefined-var-template -Wno-constant-conversion -Wno-inconsistent-missing-override
        -Wno-deprecated-builtins -Wno-unused-command-line-argument -Wno-nontrivial-memcall)
    endif()
  else() # clang on Linux and Android
    dagor_compile_options("${_c_cxx}" -Wno-unused-value -Wabsolute-value -Wno-inline-new-delete
      -Wno-unknown-warning-option -Wno-deprecated-register -Wno-address-of-packed-member -Wno-expansion-to-defined
      -Wno-logical-not-parentheses -Wno-c++1z-compat -Wno-undefined-var-template -Wno-inconsistent-missing-override
      -Wno-deprecated-builtins -Wno-nontrivial-memcall -fdiagnostics-absolute-paths)
  endif()
endif()

# --- the platform: definitions, system libraries, link settings (platform/<CMAKE_SYSTEM_NAME>.cmake) ------------------
include("${DAGOR_PLATFORM_FILE}")

# --- link settings of the compilers -----------------------------------------------------------------------------------
# GNU-style linkers resolve a static library only against what comes before it, and the engine's libraries need each
# other both ways (osApiWrappers, perfMon, memory and kernel, ...): a program's libraries link as one group
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Android)$")
  foreach(_lang C CXX)
    foreach(_rule LINK_EXECUTABLE CREATE_SHARED_LIBRARY CREATE_SHARED_MODULE)
      string(REPLACE "<LINK_LIBRARIES>" "-Wl,--start-group <LINK_LIBRARIES> -Wl,--end-group" CMAKE_${_lang}_${_rule}
        "${CMAKE_${_lang}_${_rule}}")
    endforeach()
  endforeach()
  unset(_lang)
  unset(_rule)
endif()
if(MSVC AND DAGOR_VARIANT STREQUAL "maxplug")
  # the DLL CRT and never the static one (3ds Max loads the plugins)
  dagor_link_options("${_linked}" /DEBUG /INCREMENTAL:NO /NODEFAULTLIB:LIBC /NODEFAULTLIB:LIBCP /NODEFAULTLIB:LIBCMT
    /NODEFAULTLIB:LIBCPMT)
  dagor_link_options("$<AND:${_linked},$<NOT:${_dbg}>>" /OPT:REF)
elseif(MSVC)
  # the static CRT (CMAKE_MSVC_RUNTIME_LIBRARY) and never the DLL one a third-party object might ask for
  dagor_link_options("${_linked}" /DEBUG /INCREMENTAL:NO /NODEFAULTLIB:LIBMMT /NODEFAULTLIB:LIBIRC /NODEFAULTLIB:LIBC
    /NODEFAULTLIB:MSVCRT /NODEFAULTLIB:MSVCPRT /NODEFAULTLIB:UCRT /NODEFAULTLIB:VCRUNTIME)
  dagor_link_options("$<AND:${_linked},$<NOT:${_dbg}>>" /OPT:REF /NODEFAULTLIB:LIBCMTD /NODEFAULTLIB:LIBCPMTD)
  dagor_link_options("$<AND:${_linked},${_dbg}>" /NODEFAULTLIB:LIBCMT /NODEFAULTLIB:LIBCPMT)
  # /OPT:REF also folds identical code and data into one address, which breaks code comparing the addresses of
  # distinct functions or objects (daFrameGraph's blob projectors and type tags): lld-link's safe ICF keeps those, by
  # clang's address-significance tables; link.exe cannot tell them apart and does not fold at all. ASan: no folding.
  if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang" AND DAGOR_SANITIZE STREQUAL "none")
    dagor_link_options("$<AND:${_linked},$<NOT:${_dbg}>>" /OPT:SAFEICF)
  else()
    dagor_link_options("$<AND:${_linked},$<NOT:${_dbg}>>" /OPT:NOICF)
  endif()
  dagor_link_options("${_exe}" /FILEALIGN:512)
endif()

# --- sanitizers and coverage ------------------------------------------------------------------------------------------
if(NOT DAGOR_SANITIZE STREQUAL "none")
  if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    if(NOT DAGOR_SANITIZE STREQUAL "address")
      message(FATAL_ERROR "MSVC supports only DAGOR_SANITIZE=address")
    endif()
    dagor_compile_options("${_c_cxx}" /fsanitize=address)
  else()
    set(_san -fsanitize=${DAGOR_SANITIZE})
    if(DAGOR_SANITIZE STREQUAL "address")
      list(APPEND _san -fsanitize-address-use-after-scope -fsanitize-address-use-after-return=always)
    elseif(DAGOR_SANITIZE STREQUAL "undefined")
      list(APPEND _san -fsanitize-ignorelist=${DAGOR_PROG_DIR}/ubsan.ignore)
    endif()
    dagor_compile_options("${_c_cxx}" ${_san})
    if(MSVC) # clang-cl
      if(NOT DAGOR_SANITIZE STREQUAL "address" OR NOT DAGOR_ARCH STREQUAL "x86_64")
        message(FATAL_ERROR "clang-cl builds support only DAGOR_SANITIZE=address on x86_64")
      endif()
      # lld-link has no /INFERASANLIBS: the runtime (clang_rt.asan_dynamic-x86_64.dll at run time) is linked explicitly
      link_libraries("$<${_linked}:System::clang_rt.asan_dynamic-x86_64>")
      dagor_link_options("${_linked}" /WHOLEARCHIVE:clang_rt.asan_static_runtime_thunk-x86_64.lib)
    else()
      dagor_link_options("${_linked}" -fsanitize=${DAGOR_SANITIZE})
    endif()
    unset(_san)
  endif()
  if(MSVC)
    dagor_link_options("${_linked}" /OPT:NOICF) # string-literal folding trips the asan ODR checks
  endif()
endif()

if(DAGOR_COVERAGE)
  dagor_compile_options("${_c_cxx}" -fprofile-instr-generate -fcoverage-mapping)
  if(MSVC)
    link_libraries("$<${_linked}:System::clang_rt.profile-x86_64>")
  else()
    dagor_link_options("${_linked}" -fprofile-instr-generate)
  endif()
endif()

# link-time optimization (CMAKE_INTERPROCEDURAL_OPTIMIZATION above): clang's ThinLTO and whole-program devirtualization
if(NOT DAGOR_LTO STREQUAL "OFF" AND CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  if(DAGOR_LTO STREQUAL "thin")
    dagor_compile_options("${_c_cxx}" -flto=thin)
    if(NOT MSVC)
      dagor_link_options("${_linked}" -flto=thin)
    endif()
  endif()
  if(DAGOR_LTO_DEVIRT)
    dagor_compile_options("${_cxx}" -fwhole-program-vtables)
    if(NOT MSVC)
      dagor_link_options("${_linked}" -fwhole-program-vtables)
    endif()
  endif()
endif()

# --- warning sets: DAGOR_STRICT_OPTIONS for first-party code, DAGOR_LAX_OPTIONS for third-party ------------------------
set(DAGOR_STRICT_OPTIONS)
set(DAGOR_LAX_OPTIONS)
if(MSVC AND CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  foreach(_w unused-parameter unused-variable unused-lambda-capture range-loop-construct pessimizing-move redundant-move
             self-move)
    list(APPEND DAGOR_STRICT_OPTIONS "$<${_cxx}:-W${_w}>" "$<${_cxx}:-Werror=${_w}>")
  endforeach()
  list(APPEND DAGOR_STRICT_OPTIONS "$<${_cxx}:/permissive->")
  # the stack frame limit of the shipped configurations; sanitizer redzones inflate frames, so their size says nothing
  # about the shipped binary
  if(DAGOR_SANITIZE STREQUAL "none")
    set(_limit "$<IF:$<BOOL:$<TARGET_PROPERTY:DAGOR_FRAME_LIMIT>>,$<TARGET_PROPERTY:DAGOR_FRAME_LIMIT>,32768>")
    list(APPEND DAGOR_STRICT_OPTIONS "$<$<AND:${_cxx},$<NOT:${_dbg}>>:/clang:-Wframe-larger-than=${_limit}>"
      "$<$<AND:${_cxx},$<NOT:${_dbg}>>:-Werror=frame-larger-than>")
    unset(_limit)
  endif()
elseif(MSVC)
  set(_wd 4514 4061 4820 4668 4619 4365 4127 4302 4242 4244 4265 4101 4201 4625 4626 4800 4018 4710 4245 4291 4389
    4200 4255 4711 4062 4355 4640 4305 4324 4511 4512 4738 4996 4005 4740 4702 4826 4503 4748 4987 4574 4554 4471
    4350 4370 4371 4316 4388 4091 5026 5027 4774 4312 4334 5220 5219 4464 4463 4589 4595 4435 4319 4311 4267 4477
    4777 4548 5039 5045 4623 5038 4768 4456 5052 5204 4577 4643 4866 4868 5245 5246 5264)
  list(TRANSFORM _wd PREPEND /wd)
  list(APPEND DAGOR_STRICT_OPTIONS -Wall ${_wd} /permissive-)
  set(_wd 4244 4101 4800 4018 4291 4200 4355 4305 4996 4005 4740 4748 4324 4503 4574 4554 4316 4388 4091 5026 5027
    4334 4595 4838 4312 4302 4311 4319 4477 5039 5045 4623 5038 4768 5204 4577 4267 4643 4723 4866)
  list(TRANSFORM _wd PREPEND /wd)
  list(APPEND DAGOR_LAX_OPTIONS -W3 ${_wd})
  list(TRANSFORM DAGOR_STRICT_OPTIONS REPLACE "^(.+)$" "$<${_c_cxx}:\\1>")
  list(TRANSFORM DAGOR_LAX_OPTIONS REPLACE "^(.+)$" "$<${_c_cxx}:\\1>")
  unset(_wd)
elseif(CMAKE_CXX_COMPILER_ID MATCHES "^(GNU|LCC)$")
  list(APPEND DAGOR_STRICT_OPTIONS "$<${_cxx}:-Wunused-parameter>")
else() # clang
  foreach(_w unused-lambda-capture range-loop-construct)
    list(APPEND DAGOR_STRICT_OPTIONS "$<${_cxx}:-W${_w}>" "$<${_cxx}:-Werror=${_w}>")
  endforeach()
  if(NOT APPLE)
    list(APPEND DAGOR_STRICT_OPTIONS "$<${_cxx}:-Wunused-parameter>")
  endif()
endif()
unset(_w)

# dagor_deterministic_fp(<options-var> [KEEP_TRAPPING_MATH] [KEEP_NANS]): appends to <options-var> the options that give
# floating point the same results with every compiler and platform, for the code the network or the content depend on
# (physics, collision, land and rendinst positions): no unsafe math, no contraction, no fused multiply-adds, and
# -fno-trapping-math unless KEEP_TRAPPING_MATH. KEEP_NANS is for code that checks for NaNs and the sign of zero, which
# the fast math of the rest assumes away. MSVC needs none of them. The code's v_madd must be VECMATH_NO_FMA too (NEON's
# vfmaq ignores contraction).
function(dagor_deterministic_fp var)
  cmake_parse_arguments(PARSE_ARGV 1 arg "KEEP_TRAPPING_MATH;KEEP_NANS" "" "")
  if(NOT CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
    return()
  endif()
  set(x -)
  if(MSVC)
    set(x /clang:-)
  endif()
  set(options ${${var}})
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    list(APPEND options -Wno-overriding-option) # -fno-trapping-math after -fno-unsafe-math-optimizations
    if(NOT WIN32)
      list(APPEND options -Wno-overriding-t-option) # the same, for older clang
    endif()
  endif()
  list(APPEND options ${x}fno-unsafe-math-optimizations)
  if(NOT arg_KEEP_TRAPPING_MATH)
    list(APPEND options ${x}fno-trapping-math)
  endif()
  list(APPEND options ${x}ffp-contract=off)
  if(arg_KEEP_NANS)
    list(APPEND options ${x}fno-finite-math-only ${x}fsigned-zeros)
  endif()
  if(DAGOR_ARCH STREQUAL "x86_64")
    list(APPEND options ${x}mno-fma)
  endif()
  set(${var} "${options}" PARENT_SCOPE)
endfunction()

foreach(_var c_cxx cxx dev rel dbg release exe linked checked stack_protection exceptions exc_prop seh rtti_default rtti
             cxx_exceptions cxx_no_exceptions opt unopt sp no_sp cfg)
  unset(_${_var})
endforeach()
unset(_var)
