# the dirs of prog/gameLibs/vehiclePhys: the vehicle exporter is a daBuild plugin, on daKernel
if(DAGOR_KERNEL_LINKAGE STREQUAL "dynamic" AND NOT DAGOR_SANITIZE STREQUAL "address")
  add_subdirectory(exporters)
endif()
