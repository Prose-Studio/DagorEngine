# Breakpad's common Linux code: ELF symbols and ids, memory-mapped files, the C library helpers of its client
dagor_add_library(3rdPartyLibs.breakpad.common.linux LAX dump_symbols.cc elf_symbols_to_module.cc file_id.cc
  guid_creator.cc synth_elf.cc elfutils.cc linux_libc_support.cc memory_mapped_file.cc safe_readlink.cc crc32.cc)
target_include_directories(3rdPartyLibs.breakpad.common.linux PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad)
target_compile_options(3rdPartyLibs.breakpad.common.linux PRIVATE -Wno-unused-parameter)
