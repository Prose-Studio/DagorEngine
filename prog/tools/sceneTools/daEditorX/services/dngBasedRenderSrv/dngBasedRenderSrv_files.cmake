set(FILES dngBasedRender.cpp dngSkiesSrv.cpp)
set(ES_FILES renderServicesES.cpp.inl)
# the damage events of daNetGameLibs/dm, where it is there
if(EXISTS "${DAGOR_PROG_DIR}/daNetGameLibs/dm/damageEvents.h")
  set_property(SOURCE dngBasedRender.cpp APPEND PROPERTY COMPILE_DEFINITIONS HAVE_DNGLIB_DM)
endif()
