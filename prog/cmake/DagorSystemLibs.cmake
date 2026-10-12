# The libraries of the system and the toolchain as imported targets, System::<name> (CMAKE_LINK_LIBRARIES_ONLY_TARGETS
# makes every link item that could name a target name one): target_link_libraries(<target> PRIVATE System::ws2_32).
#
# dagor_system_library(<name>...) declares System::<name> for the import library or shared object <name> the linker finds
# on its own (IMPORTED_LIBNAME). On Linux each is looked up once: a missing one is reported with the package that has
# it, as a warning (only the programs that link it fail), so a server box needs no GUI packages.
include_guard(GLOBAL)

# library -> package, for the apt (Debian, Ubuntu, Astra) and dnf/urpmi (Fedora, CentOS, ROSA, ALT) families
set(_dagor_pkg_apt_X11 libx11-dev)
set(_dagor_pkg_apt_Xrandr libxrandr-dev)
set(_dagor_pkg_apt_Xcursor libxcursor-dev)
set(_dagor_pkg_apt_Xi libxi-dev)
set(_dagor_pkg_apt_xkbcommon libxkbcommon-dev)
set(_dagor_pkg_apt_xkbfile libxkbfile-dev)
set(_dagor_pkg_apt_fltk libfltk1.3-dev)
set(_dagor_pkg_apt_udev libudev-dev)
set(_dagor_pkg_apt_pulse libpulse-dev)
set(_dagor_pkg_apt_asound libasound2-dev)
set(_dagor_pkg_apt_uuid uuid-dev)
set(_dagor_pkg_apt_curl libcurl4-openssl-dev)
set(_dagor_pkg_apt_ssl libssl-dev)
set(_dagor_pkg_apt_crypto libssl-dev)
set(_dagor_pkg_rpm_X11 libX11-devel)
set(_dagor_pkg_rpm_Xrandr libXrandr-devel)
set(_dagor_pkg_rpm_Xcursor libXcursor-devel)
set(_dagor_pkg_rpm_Xi libXi-devel)
set(_dagor_pkg_rpm_xkbcommon libxkbcommon-devel)
set(_dagor_pkg_rpm_xkbfile libxkbfile-devel)
set(_dagor_pkg_rpm_fltk fltk-devel)
set(_dagor_pkg_rpm_udev systemd-devel)
set(_dagor_pkg_rpm_pulse pulseaudio-libs-devel)
set(_dagor_pkg_rpm_asound alsa-lib-devel)
set(_dagor_pkg_rpm_uuid libuuid-devel)
set(_dagor_pkg_rpm_curl libcurl-devel)
set(_dagor_pkg_rpm_ssl openssl-devel)
set(_dagor_pkg_rpm_crypto openssl-devel)
# provided by the C library or the toolchain, never looked up
set(_dagor_system_libs_builtin c m rt pthread dl stdc++ c++ log android)

function(dagor_system_library)
  foreach(name IN LISTS ARGN)
    if(TARGET System::${name})
      continue()
    endif()
    add_library(System::${name} INTERFACE IMPORTED GLOBAL)
    set_property(TARGET System::${name} PROPERTY IMPORTED_LIBNAME "${name}")
    if(LINUX AND NOT name IN_LIST _dagor_system_libs_builtin AND NOT CMAKE_CROSSCOMPILING)
      find_library(DAGOR_SYSTEM_LIB_${name} NAMES ${name})
      if(NOT DAGOR_SYSTEM_LIB_${name})
        if(EXISTS /usr/bin/apt-get)
          set(package "${_dagor_pkg_apt_${name}}")
          set(install "sudo apt-get install")
        else()
          set(package "${_dagor_pkg_rpm_${name}}")
          set(install "sudo dnf install")
        endif()
        if(NOT package)
          set(package "<the development package of lib${name}>")
        endif()
        message(STATUS "System library ${name} is missing, the programs that link it will not build: ${install} ${package}")
      endif()
    endif()
  endforeach()
endfunction()

# the toolchain's own (the C and C++ runtimes, the clang runtime libraries of the sanitizers and coverage)
if(WIN32)
  dagor_system_library(kernel32 user32 gdi32 ole32 oleaut32 winmm dbghelp advapi32 shell32 shlwapi ws2_32 wsock32
    iphlpapi version comdlg32 comctl32 uuid imm32 setupapi hid dxgi d3d11 d3d12 d3dcompiler dxguid dinput8 xinput
    psapi userenv crypt32 bcrypt secur32 normaliz wldap32 winhttp wininet mfplat mfuuid mfreadwrite mf strmiids
    propsys dwmapi uxtheme powrprof wtsapi32 netapi32 mpr rpcrt4 synchronization wbemuuid gdiplus msimg32 opengl32
    runtimeobject dsound ncrypt delayimp wintrust
    clang_rt.builtins-x86_64 clang_rt.asan_dynamic-x86_64 clang_rt.profile-x86_64)
else()
  dagor_system_library(m rt dl pthread stdc++)
endif()
if(LINUX)
  dagor_system_library(X11 Xcursor Xrandr Xi xkbcommon xkbfile fltk udev pulse asound uuid curl ssl crypto)
endif()
find_package(Threads REQUIRED)
