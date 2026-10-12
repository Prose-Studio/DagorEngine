# find_package(Dagor) in a project's top-level CMakeLists.txt, after project(): the engine's settings and functions
# (Dagor.cmake) and its libraries and programs, as a subdirectory of the project's tree (<build>/dagor). The engine is
# built with the project's settings (its game variant, dedicated server or not), and only what the project's targets
# link is built (prog/CMakeLists.txt, a subproject of the project's tree). Dagor_DIR, which the engine's preset fragment
# sets (prog/cmake/presets/base.json), points here.
include_guard(GLOBAL)

include("${CMAKE_CURRENT_LIST_DIR}/Dagor.cmake")
add_subdirectory("${DAGOR_PROG_DIR}" "${CMAKE_BINARY_DIR}/dagor" EXCLUDE_FROM_ALL)
set(Dagor_FOUND TRUE)
