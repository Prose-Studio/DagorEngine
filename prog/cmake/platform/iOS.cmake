# iOS: the target definitions and link settings (included by DagorCompilerFlags.cmake, whose helpers and conditions it
# uses).
include("${CMAKE_CURRENT_LIST_DIR}/Apple.cmake")
dagor_compile_definitions(1 _TARGET_APPLE=2 _TARGET_IOS __APPLE_IOS__ _TARGET_ARCH_ARM64 _TARGET_SIMD_NEON
  ARM_NEON_GCC_COMPATIBILITY)
foreach(_framework Foundation UIKit QuartzCore CoreFoundation Security SystemConfiguration Metal GameController
                   AudioToolbox AVFoundation CoreMotion)
  link_libraries("$<${_linked}:$<LINK_LIBRARY:FRAMEWORK,${_framework}>>")
endforeach()
unset(_framework)
