// Copyright (C) Gaijin Games KFT.  All rights reserved.

#include "cppStcode.h"
#include "globalConfig.h"
#include "defer.h"
#include "shLog.h"
#include "semUtils.h"
#include "commonUtils.h"
#include "loadShaders.h"
#include <shaders/cppStcodeVer.h>
#include <osApiWrappers/dag_files.h>
#include <osApiWrappers/dag_direct.h>
#include <osApiWrappers/dag_dynLib.h>
#include <osApiWrappers/dag_pathDelim.h>
#include <util/dag_hash.h>
#include <util/dag_globDef.h>
#include <EASTL/string.h>
#include <generic/dag_enumerate.h>
#include <dag/dag_vectorSet.h>


#if _TARGET_PC_WIN
#include <windows.h>
#include <direct.h>
#else
#include <unistd.h>
#endif

static constexpr char STCODE_VER_FILE_NAME[] = "ver.txt";

eastl::optional<shader_layout::ExternalStcodeMode> arg_str_to_cpp_stcode_mode(const char *str)
{
  if (streq(str, "regular"))
    return shader_layout::ExternalStcodeMode::BRANCHLESS_CPP;
  else if (streq(str, "branches"))
    return shader_layout::ExternalStcodeMode::BRANCHED_CPP;
  else
    return eastl::nullopt;
}

static constexpr const char *CONFIG_NAMES[] = {"dev", "rel", "dbg"};
static constexpr const char *CONFIG_SUFFICES[] = {"-dev", "", "-dbg"};
static constexpr const char *CONFIG_BUILD_NAMES[] = {"Dev", "Rel", "Dbg"}; // the engine's configurations

static const char *config_to_build_name(StcodeDynlibConfig config) { return CONFIG_BUILD_NAMES[size_t(config)]; }
static const char *config_to_mangled_suffix(StcodeDynlibConfig config) { return CONFIG_SUFFICES[size_t(config)]; }

bool set_stcode_config_from_arg(const char *str, shc::CompilerConfig &config_rw)
{
  for (auto [id, name] : enumerate(CONFIG_NAMES))
  {
    if (streq(name, str))
    {
      config_rw.cppStcodeCompConfig = StcodeDynlibConfig(id);
      return true;
    }
  }
  return false;
}

static const char *arch_name(StcodeTargetArch arch)
{
  switch (arch)
  {
    case StcodeTargetArch::DEFAULT: return "<default>";
    case StcodeTargetArch::X86: return "x86";
    case StcodeTargetArch::X86_64: return "x86_64";
    case StcodeTargetArch::ARM64: return "arm64";
    case StcodeTargetArch::ARM64_E: return "arm64e";
    case StcodeTargetArch::ARM_V7: return "armv7";
    case StcodeTargetArch::ARM_V7S: return "armv7s";
    case StcodeTargetArch::ARMEABI_V7A: return "armeabi-v7a";
    case StcodeTargetArch::ARM64_V8A: return "arm64-v8a";
    case StcodeTargetArch::I386: return "i386";
    case StcodeTargetArch::E2K: return "e2k";
    case StcodeTargetArch::MAC_X86_64_ARM64_UNIVERSAL: return "x86_64";
    case StcodeTargetArch::ARM64_EC: return "arm64ec";
  }
  return nullptr;
}

// the arch as the engine's build names it (DAGOR_ARCH), nullptr for those it doesn't build
static const char *arch_name_for_build(StcodeTargetArch arch)
{
  switch (arch)
  {
    case StcodeTargetArch::X86_64: return "x86_64";
    case StcodeTargetArch::ARM64:
    case StcodeTargetArch::ARM64_V8A:
    case StcodeTargetArch::ARM64_E: return "arm64";
    case StcodeTargetArch::MAC_X86_64_ARM64_UNIVERSAL: return "universal";
    case StcodeTargetArch::E2K: return "e2k";
    default: return nullptr;
  }
}

static const char *arch_name_for_dll_name(StcodeTargetArch arch)
{
  switch (arch)
  {
    case StcodeTargetArch::DEFAULT: G_ASSERTF(0, "Arch must be decided for dll name");
    case StcodeTargetArch::X86:
    case StcodeTargetArch::I386: return "x86";
    case StcodeTargetArch::X86_64: return "x86_64";
    case StcodeTargetArch::ARM64:
    case StcodeTargetArch::ARM64_V8A:
    case StcodeTargetArch::ARM64_E: return "arm64";
    case StcodeTargetArch::ARM_V7:
    case StcodeTargetArch::ARM_V7S:
    case StcodeTargetArch::ARMEABI_V7A: return "armv7";
    case StcodeTargetArch::E2K: return "e2k";
    case StcodeTargetArch::MAC_X86_64_ARM64_UNIVERSAL: return "universal";
    case StcodeTargetArch::ARM64_EC: return "arm64ec";
  }
  return nullptr;
}

static bool arch_and_platform_is_fixed_for_shaders()
{
#if _CROSS_TARGET_C1 | _CROSS_TARGET_C2

#elif _CROSS_TARGET_DX12
  return shc::config().targetPlatform != dx12::dxil::Platform::PC;
#elif _CROSS_TARGET_SPIRV
  return shc::config().cppStcodePlatform == StcodeTargetPlatform::NSWITCH;
#else
  return false;
#endif
}

static bool validate_arch(StcodeTargetArch arch)
{
#if _CROSS_TARGET_DX12
  if (shc::config().targetPlatform != dx12::dxil::Platform::PC)
    return arch == StcodeTargetArch::X86_64 || arch == StcodeTargetArch::ARM64;
  else
    return item_is_in(arch, {StcodeTargetArch::X86, StcodeTargetArch::X86_64, StcodeTargetArch::ARM64, StcodeTargetArch::ARM64_EC});
#elif _CROSS_TARGET_DX11
  return item_is_in(arch, {StcodeTargetArch::X86, StcodeTargetArch::X86_64, StcodeTargetArch::ARM64, StcodeTargetArch::ARM64_EC});
#elif _CROSS_TARGET_C1 | _CROSS_TARGET_C2

#elif _CROSS_TARGET_SPIRV
#if _TARGET_PC_WIN
  return item_is_in(arch,
    {StcodeTargetArch::DEFAULT, StcodeTargetArch::X86, StcodeTargetArch::X86_64, StcodeTargetArch::E2K, StcodeTargetArch::ARM64,
      StcodeTargetArch::ARM64_EC, StcodeTargetArch::ARMEABI_V7A, StcodeTargetArch::ARM64_V8A});
#elif _TARGET_PC_LINUX
  return item_is_in(arch, {StcodeTargetArch::DEFAULT, StcodeTargetArch::X86_64, StcodeTargetArch::E2K, StcodeTargetArch::ARM64,
                            StcodeTargetArch::ARMEABI_V7A, StcodeTargetArch::ARM64_V8A});
#elif _TARGET_PC_MACOSX
  return item_is_in(arch, {StcodeTargetArch::ARMEABI_V7A, StcodeTargetArch::ARM64_V8A});
#endif
#elif _CROSS_TARGET_METAL
  return item_is_in(arch,
    {StcodeTargetArch::DEFAULT, StcodeTargetArch::X86_64, StcodeTargetArch::ARM64, StcodeTargetArch::ARM64_E, StcodeTargetArch::ARM_V7,
      StcodeTargetArch::ARM_V7S, StcodeTargetArch::I386, StcodeTargetArch::MAC_X86_64_ARM64_UNIVERSAL});
#elif _CROSS_TARGET_EMPTY
  return false;
#else
#error Unknown target
#endif
}

#if _CROSS_TARGET_DX12
template <typename T>
static T platform_switch(T &&if_pc, T &&if_xboxone, T &&if_scarlett)
{
  switch (shc::config().targetPlatform)
  {
    case dx12::dxil::Platform::PC: return eastl::forward<T>(if_pc);
    case dx12::dxil::Platform::XBOX_ONE: return eastl::forward<T>(if_xboxone);
    case dx12::dxil::Platform::XBOX_SCARLETT: return eastl::forward<T>(if_scarlett);
    default: G_ASSERT_RETURN(0, eastl::forward<T>(if_pc));
  }
}
#endif

static bool validate_arch_for_platform(const shc::CompilerConfig &config, StcodeTargetArch arch);

#if _CROSS_TARGET_SPIRV

static bool validate_arch_for_platform(const shc::CompilerConfig &config, StcodeTargetArch arch)
{
  return arch == StcodeTargetArch::DEFAULT || config.cppStcodePlatform == StcodeTargetPlatform::DEFAULT ||
         (config.cppStcodePlatform == StcodeTargetPlatform::NSWITCH && arch == StcodeTargetArch::ARM64) ||
         (config.cppStcodePlatform == StcodeTargetPlatform::ANDROID &&
           item_is_in(arch, {StcodeTargetArch::ARMEABI_V7A, StcodeTargetArch::ARM64_V8A})) ||
#if _TARGET_PC_WIN
         (config.cppStcodePlatform == StcodeTargetPlatform::PC &&
           item_is_in(arch, {StcodeTargetArch::X86, StcodeTargetArch::X86_64, StcodeTargetArch::ARM64, StcodeTargetArch::ARM64_EC}));
#elif _TARGET_PC_LINUX
         (config.cppStcodePlatform == StcodeTargetPlatform::PC && item_is_in(arch, {StcodeTargetArch::X86_64, StcodeTargetArch::E2K}));
#elif _TARGET_PC_MACOSX
         false; // android and {armv7a, armv8a} is already listed in common code above
#endif
}

bool set_stcode_platform_from_arg(const char *str, shc::CompilerConfig &config)
{
  if (strcmp(str, "pc") == 0)
    config.cppStcodePlatform = StcodeTargetPlatform::PC;
  else if (strcmp(str, "android") == 0)
    config.cppStcodePlatform = StcodeTargetPlatform::ANDROID;
  else if (strcmp(str, "nswitch") == 0)
    config.cppStcodePlatform = StcodeTargetPlatform::NSWITCH;
  else
    return false;

  for (StcodeTargetArch arch : config.cppStcodeArchs)
  {
    if (!validate_arch_for_platform(config, arch))
      return false;
  }
  return true;
}

template <typename T>
static T platform_switch(T &&if_pc, T &&if_android, T &&if_nswitch)
{
  switch (shc::config().cppStcodePlatform)
  {
    case StcodeTargetPlatform::DEFAULT:
    case StcodeTargetPlatform::PC: return eastl::forward<T>(if_pc);
    case StcodeTargetPlatform::ANDROID: return eastl::forward<T>(if_android);
    case StcodeTargetPlatform::NSWITCH: return eastl::forward<T>(if_nswitch);
    default: G_ASSERT_RETURN(0, eastl::forward<T>(if_pc));
  }
}

#elif _CROSS_TARGET_METAL

static bool validate_arch_for_platform(const shc::CompilerConfig &config, StcodeTargetArch arch)
{
  return arch == StcodeTargetArch::DEFAULT || config.cppStcodePlatform == StcodeTargetPlatform::DEFAULT ||
         (config.cppStcodePlatform == StcodeTargetPlatform::MACOSX &&
           item_is_in(arch, {StcodeTargetArch::X86_64, StcodeTargetArch::ARM64, StcodeTargetArch::MAC_X86_64_ARM64_UNIVERSAL})) ||
         (config.cppStcodePlatform == StcodeTargetPlatform::IOS &&
           item_is_in(arch, {StcodeTargetArch::ARM64, StcodeTargetArch::ARM64_E, StcodeTargetArch::ARM_V7, StcodeTargetArch::ARM_V7S,
                              StcodeTargetArch::I386}));
}

bool set_stcode_platform_from_arg(const char *str, shc::CompilerConfig &config)
{
  if (strcmp(str, "macosx") == 0)
    config.cppStcodePlatform = StcodeTargetPlatform::MACOSX;
  else if (strcmp(str, "ios") == 0)
    config.cppStcodePlatform = StcodeTargetPlatform::IOS;
  else
    return false;

  for (StcodeTargetArch arch : config.cppStcodeArchs)
  {
    if (!validate_arch_for_platform(config, arch))
      return false;
  }
  return true;
}

static bool is_ios() { return shc::config().cppStcodePlatform == StcodeTargetPlatform::IOS; }

template <typename T>
static T if_ios(T &&if_true, T &&if_false)
{
  if (is_ios())
    return eastl::forward<T>(if_true);
  else
    return eastl::forward<T>(if_false);
}

#else

static bool validate_arch_for_platform(const shc::CompilerConfig &, StcodeTargetArch) { return true; }
#if _CROSS_TARGET_EMPTY
template <typename T>
static T platform_switch(T &&if_pc, T &&, T &&)
{
  return if_pc;
}
#endif

#endif

bool add_stcode_arch_from_arg(const char *str, shc::CompilerConfig &config_rw)
{
  StcodeTargetArch res = StcodeTargetArch::DEFAULT;
#if _TARGET_PC_MACOSX
  if (streq(str, "universal"))
    res = StcodeTargetArch::MAC_X86_64_ARM64_UNIVERSAL;
  else
#endif
  {
    for (StcodeTargetArch arch : ALL_STCODE_ARCHS)
    {
      if (arch != StcodeTargetArch::DEFAULT && strcmp(str, arch_name(arch)) == 0)
      {
        res = arch;
        break;
      }
    }
  }
  if (res == StcodeTargetArch::DEFAULT) // Not found or invalid
    return false;


  config_rw.cppStcodeArchs.push_back(res);

  return validate_arch(res) && validate_arch_for_platform(config_rw, res);
}

static void replace_char(char *str, size_t len, char old_ch, char new_ch)
{
  for (char *p = str; p != str + len; ++p)
  {
    if (*p == old_ch)
      *p = new_ch;
  }
}

StcodeCompilationDirs init_stcode_compilation(const char *dest_dir, const char *shortened_dest_dir_for_caching)
{
  RET_IF_SHOULD_NOT_COMPILE({});

  StcodeCompilationDirs dirs{};

  dirs.stcodeDir = string_f("%s/stcode", dest_dir);
  dirs.stcodeCompilationCacheDirUnmangled = shortened_dest_dir_for_caching;

  dd_simplify_fname_c(dirs.stcodeDir.data());
  dirs.stcodeDir.resize(strlen(dirs.stcodeDir.c_str()));
  replace_char(dirs.stcodeDir.data(), dirs.stcodeDir.length(), '\\', '/');

  if (!dd_dir_exist(dirs.stcodeDir.c_str()))
    dd_mkdir(dirs.stcodeDir.c_str());

  return dirs;
}

static void write_file(const char *fn, const char *src, size_t src_len)
{
  file_ptr_t f = df_open(fn, DF_WRITE | DF_CREATE);
  if (!f)
  {
    sh_debug(SHLOG_ERROR, "Failed to open file %s for write", fn);
    return;
  }
  int charsWritten = df_write(f, src, src_len);
  if (charsWritten != src_len)
    sh_debug(SHLOG_ERROR, "Failed write full file (%s)", fn);

  df_close(f);
  return;
}

// a build file the build tool watches: rewritten only when it changes, so the build is not configured again for nothing
static void write_file_if_changed(const char *fn, const eastl::string &src)
{
  if (file_ptr_t f = df_open(fn, DF_READ))
  {
    eastl::string old;
    old.resize(df_length(f));
    const bool same = df_read(f, old.data(), int(old.size())) == int(old.size()) && old == src;
    df_close(f);
    if (same)
      return;
  }
  write_file(fn, src.c_str(), src.length());
}

static constexpr char CPPFILE_HEADER_TEMPLATE[] = "/* xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx */\n";
static constexpr size_t CPPFILE_HEADER_LEN = LITSTR_LEN(CPPFILE_HEADER_TEMPLATE);
static constexpr char CPPFILE_HEADER_FMT[] =
  "/* %02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx */\n";
static constexpr char STAMP_HEADER_TEMPLATE[] = "# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n";
static constexpr size_t STAMP_HEADER_LEN = LITSTR_LEN(STAMP_HEADER_TEMPLATE);
static constexpr char STAMP_HEADER_FMT[] =
  "# %02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx\n";

template <size_t HEADER_LEN, auto HEADER_TEMPLATE>
static eastl::optional<BlkHashBytes> extract_blk_hash_from_read_header(const char (&buf)[HEADER_LEN])
{
  constexpr eastl::string_view HT{HEADER_TEMPLATE};

  // @TODO: match other parts of the header?

  // Only lower-case
  const auto hexDigitToNum = [](char digit) -> eastl::optional<uint8_t> {
    if (digit >= 'a' && digit <= 'f')
      return 10 + (digit - 'a');
    if (digit >= '0' && digit <= '9')
      return digit - '0';
    else
      return eastl::nullopt;
  };

  BlkHashBytes res{};
  for (auto readId = HT.find('x'); unsigned char &dc : res)
  {
    G_ASSERT(HT[readId] == 'x' && HT[readId + 1] == 'x');

    uint8_t hi, lo;

    if (auto hiMaybe = hexDigitToNum(buf[readId++]))
      hi = *hiMaybe;
    else
      return eastl::nullopt;

    if (auto loMaybe = hexDigitToNum(buf[readId++]))
      lo = *loMaybe;
    else
      return eastl::nullopt;

    dc = (hi << 4) | lo;
  }

  return res;
}

template <size_t HEADER_LEN, auto HEADER_FMT, size_t... Is>
  requires(sizeof...(Is) == eastl::tuple_size_v<BlkHashBytes>)
static eastl::string make_header_from_blk_hash_impl(eastl::index_sequence<Is...>, const BlkHashBytes &hash)
{
  const auto res = string_f(HEADER_FMT, (hash[Is])...);
  G_ASSERT(res.length() == HEADER_LEN);
  return res;
}

template <size_t HEADER_LEN, auto HEADER_FMT>
static eastl::string make_header_from_blk_hash(const BlkHashBytes &hash)
{
  return make_header_from_blk_hash_impl<HEADER_LEN, HEADER_FMT>(eastl::make_index_sequence<eastl::tuple_size_v<BlkHashBytes>>{}, hash);
}

static eastl::string get_filename_from_source_name_impl(const char *shader_source_name, size_t name_len, const char *ext)
{
  const char *begin = dd_get_fname(shader_source_name);
  const char *end = dd_get_fname_ext(shader_source_name);
  if (!end)
    end = shader_source_name + name_len;

  G_ASSERT(end - begin > 0);

  return eastl::string(begin, end - begin) + eastl::string(ext);
}

static eastl::string get_cpp_filename_from_source_name(const char *shader_source_name, size_t name_len)
{
  return get_filename_from_source_name_impl(shader_source_name, name_len, ".stcode.gen.cpp");
}

static eastl::string get_header_filename_from_source_name(const char *shader_source_name, size_t name_len)
{
  return get_filename_from_source_name_impl(shader_source_name, name_len, ".stcode.gen.h");
}

void save_compiled_cpp_stcode(StcodeShader &&cpp_shader, const ShCompilationInfo &comp)
{
  RET_IF_SHOULD_NOT_COMPILE();

  // @NOTE: save even empty files: this is done so that incremental compilation can still check them for blk hash

  constexpr char headerTemplate[] =
#include "_stcodeTemplates/codeFile.h.fmt"
    ;
  constexpr char cppTemplate[] =
#include "_stcodeTemplates/codeFile.cpp.fmt"
    ;

  StcodeStrings codeStrings = cpp_shader.code.release();
  StcodeGlobalVars::Strings globvarsStrings = cpp_shader.globVars.releaseAssembledCode();

  const char *stcodeDir = comp.stcodeDirs().stcodeDir.c_str();

  const eastl::string headerFileName(eastl::string::CtorSprintf{}, "%s/%s.stcode.gen.h", stcodeDir, cpp_shader.shaderName.c_str());
  const eastl::string cppFileName(eastl::string::CtorSprintf{}, "%s/%s.stcode.gen.cpp", stcodeDir, cpp_shader.shaderName.c_str());

  const eastl::string blkHashHeader = make_header_from_blk_hash<CPPFILE_HEADER_LEN, CPPFILE_HEADER_FMT>(comp.targetBlkHash());

  const eastl::string headerSource(eastl::string::CtorSprintf{}, headerTemplate, blkHashHeader.c_str(), cpp_shader.shaderName.c_str(),
    cpp_shader.shaderName.c_str(), codeStrings.headerCode.c_str());
  const eastl::string cppSource(eastl::string::CtorSprintf{}, cppTemplate, blkHashHeader.c_str(), cpp_shader.shaderName.c_str(),
    cpp_shader.shaderName.c_str(), globvarsStrings.fetchersOrFwdCppCode.c_str(), cpp_shader.shaderName.c_str(),
    codeStrings.cppCode.c_str());

  write_file(headerFileName.c_str(), headerSource.c_str(), headerSource.length());
  write_file(cppFileName.c_str(), cppSource.c_str(), cppSource.length());
}

void save_stcode_global_vars(StcodeGlobalVars &&cpp_globvars, const ShCompilationInfo &comp, const shc::TargetContext &ctx)
{
  RET_IF_SHOULD_NOT_COMPILE();

  constexpr char cppTemplate[] =
#include "_stcodeTemplates/globVars.cpp.fmt"
    ;

  StcodeGlobalVars::Strings code = cpp_globvars.releaseAssembledCode();
  auto samplerIdsDecl = build_sampler_id_defs(ctx);

  const char *stcodeDir = comp.stcodeDirs().stcodeDir.c_str();

  const eastl::string cppFileName(eastl::string::CtorSprintf{}, "%s/glob_shadervars.stcode.gen.cpp", stcodeDir);
  const eastl::string blkHashHeader = make_header_from_blk_hash<CPPFILE_HEADER_LEN, CPPFILE_HEADER_FMT>(comp.targetBlkHash());

  const eastl::string cppSource(eastl::string::CtorSprintf{}, cppTemplate, blkHashHeader.c_str(), code.cppCode.c_str(),
    samplerIdsDecl.c_str(), code.fetchersOrFwdCppCode.c_str());

  write_file(cppFileName.c_str(), cppSource.c_str(), cppSource.length());
}

void save_stcode_refined_block(StcodeShader &cpp_stcode, const ShCompilationInfo &comp)
{
  RET_IF_SHOULD_NOT_COMPILE();

  constexpr char cppTemplate[] =
#include "_stcodeTemplates/refinedBlock.cpp.fmt"
    ;

  StcodeStrings codeStrings = cpp_stcode.code.release();

  const char *stcodeDir = comp.stcodeDirs().stcodeDir.c_str();
  const eastl::string cppFileName(eastl::string::CtorSprintf{}, "%s/glob_refined_block.stcode.gen.cpp", stcodeDir);
  const eastl::string blkHashHeader = make_header_from_blk_hash<CPPFILE_HEADER_LEN, CPPFILE_HEADER_FMT>(comp.targetBlkHash());

  const eastl::string cppSource(eastl::string::CtorSprintf{}, cppTemplate, blkHashHeader.c_str(), codeStrings.cppCode.c_str());

  write_file(cppFileName.c_str(), cppSource.c_str(), cppSource.length());
}

static auto make_hash_byte_array_initializer(const CryptoHash &hash)
{
  auto res = string_f("0x%02x", hash.data[0]);
  for (uint8_t byte : make_span_const(hash.data).subspan(1))
    res.append_sprintf(", 0x%02x", byte);
  return res;
}

void save_stcode_dll_main(StcodeShader &&combined_cppstcode, const CryptoHash &stcode_hash, const ShCompilationInfo &comp)
{
  RET_IF_SHOULD_NOT_COMPILE();

  constexpr char cppTemplate[] =
#include "_stcodeTemplates/main.cpp.fmt"
    ;

  auto [regTableCode, dynPointerTableCode, statPointerTable] = combined_cppstcode.releaseAssembledInterfaceCode();

  const char *stcodeDir = comp.stcodeDirs().stcodeDir.c_str();

  const eastl::string cppFileName(eastl::string::CtorSprintf{}, "%s/stcode_main.stcode.gen.cpp", stcodeDir);

  const eastl::string blkHashHeader = make_header_from_blk_hash<CPPFILE_HEADER_LEN, CPPFILE_HEADER_FMT>(comp.targetBlkHash());

  // For unity build, paste cpps as is. Otherwise, use headers for fwd decl
  const char *includesExtForBuildType = shc::config().cppStcodeUnityBuild ? "cpp" : "h";

  eastl::string includes;

  {
    StcodeBuilder strBuilder{};
    dag::VectorSet<eastl::string> requiredHeaders{};
    for (const String &shname : comp.sources())
    {
      eastl::string headerFileName = get_header_filename_from_source_name(shname.c_str(), shname.length());
      eastl::string filePath = eastl::string{stcodeDir} + "/" + headerFileName;
      if (dd_file_exist(filePath.c_str()))
      {
        strBuilder.emplaceBackFmt("#include \"%s\"\n", headerFileName.c_str());
        requiredHeaders.insert(eastl::move(filePath));
      }
    }

    includes = strBuilder.release();

    // Cleanup stale files
    for (const alefind_t &ff : dd_find_iterator((eastl::string{stcodeDir} + "/*.stcode.gen.h").c_str(), DA_FILE))
    {
      const eastl::string fullPath = eastl::string{stcodeDir} + "/" + ff.name;
      if (requiredHeaders.find(fullPath) == requiredHeaders.end())
        dd_erase(fullPath.c_str());
    }
  }

  const eastl::string cppSource(eastl::string::CtorSprintf{}, cppTemplate, blkHashHeader.c_str(), includes.c_str(),
    regTableCode.c_str(), dynPointerTableCode.c_str(), statPointerTable.c_str(), make_hash_byte_array_initializer(stcode_hash).c_str(),
    uint32_t(CPP_STCODE_COMMON_VER));

  write_file(cppFileName.c_str(), cppSource.c_str(), cppSource.length());
}

template <size_t HEADER_LEN, auto HEADER_TEMPLATE>
static eastl::optional<StcodeSourceFileStat> get_file_stat(const char *fn)
{
  StcodeSourceFileStat stat{};
  if (!get_file_time64(fn, stat.mtime))
    return eastl::nullopt;

  file_ptr_t f = df_open(fn, DF_READ);
  if (!f)
    return eastl::nullopt;
  DEFER([f] { df_close(f); });

  char buf[HEADER_LEN];
  if (df_read(f, buf, sizeof(buf)) != HEADER_LEN)
    return eastl::nullopt;

  auto blkHashMaybe = extract_blk_hash_from_read_header<HEADER_LEN, HEADER_TEMPLATE>(buf);
  if (!blkHashMaybe)
    return eastl::nullopt;

  stat.savedBlkHash = *blkHashMaybe;
  return stat;
}

static eastl::optional<StcodeSourceFileStat> get_files_pack_stat(std::initializer_list<const char *> filenames)
{
  StcodeSourceFileStat combinedStat{};
  for (const char *fn : filenames)
  {
    bool isCpp = strstr(fn, ".cpp") || strstr(fn, ".h");
    bool isStamp = strstr(fn, ".stamp") != nullptr;
    G_ASSERT(isCpp || isStamp);
    G_ASSERT(!(isCpp && isStamp));

    auto statMaybe = isCpp ? get_file_stat<CPPFILE_HEADER_LEN, CPPFILE_HEADER_TEMPLATE>(fn)
                           : get_file_stat<STAMP_HEADER_LEN, STAMP_HEADER_TEMPLATE>(fn);

    if (!statMaybe)
      return eastl::nullopt;

    auto &stat = *statMaybe;

    if (combinedStat.mtime < 0)
      combinedStat = stat;
    else if (combinedStat.savedBlkHash != stat.savedBlkHash)
      return eastl::nullopt;
    else
      combinedStat.mtime = min(combinedStat.mtime, stat.mtime);
  }
  return combinedStat;
}

eastl::optional<StcodeSourceFileStat> get_gencpp_files_stat(const char *target_fn, const ShCompilationInfo &comp)
{
  const char *stcodeDir = comp.stcodeDirs().stcodeDir.c_str();
  const auto fnameBase = stcode::extract_shader_name_from_path(target_fn);
  const eastl::string headerFileName{eastl::string::CtorSprintf{}, "%s/%s.stcode.gen.h", stcodeDir, fnameBase.c_str()};
  const eastl::string cppFileName{eastl::string::CtorSprintf{}, "%s/%s.stcode.gen.cpp", stcodeDir, fnameBase.c_str()};

  return get_files_pack_stat({headerFileName.c_str(), cppFileName.c_str()});
}

eastl::optional<StcodeSourceFileStat> get_main_cpp_files_stat(const ShCompilationInfo &comp)
{
  const char *stcodeDir = comp.stcodeDirs().stcodeDir.c_str();
  const eastl::string gvarFileName{eastl::string::CtorSprintf{}, "%s/glob_shadervars.stcode.gen.cpp", stcodeDir};
  const eastl::string mainFileName{eastl::string::CtorSprintf{}, "%s/stcode_main.stcode.gen.cpp", stcodeDir};
  const eastl::string stampName{eastl::string::CtorSprintf{}, "%s/stcode.stamp", stcodeDir};

  return get_files_pack_stat({gvarFileName.c_str(), mainFileName.c_str(), stampName.c_str()});
}

static int speculate_root_depth_from_path(const char *path)
{
  const char *p = path;

  // skip ../../../ ... trail
  constexpr char tail[] = "../";
  constexpr size_t tailLen = sizeof(tail) - 1;

  int rootDepthFromCwd = 0;
  for (; strncmp(p, tail, tailLen) == 0; p += tailLen)
    ++rootDepthFromCwd;

  return rootDepthFromCwd;
}

static eastl::string build_root_rel_path(int depth)
{
  if (depth == 0)
    return eastl::string(".");
  else
  {
    eastl::string res = "";
    for (int i = 0; i < depth - 1; ++i)
      res += "../";
    res += "..";
    return res;
  }
}

static eastl::string get_cwd()
{
  char buf[DAGOR_MAX_PATH * 4];
  if (getcwd(buf, sizeof(buf)))
  {
    dd_simplify_fname_c(buf);
    replace_char(buf, sizeof(buf), '\\', '/');
    return eastl::string(buf);
  }

  return eastl::string();
}

static auto split_by_lowest_dir(const char *path, size_t path_len)
{
  const char *p = strchr(path, '/');
  return p ? eastl::make_pair(eastl::string{path, size_t(p - path + 1)}, eastl::string{p + 1, path_len - (p - path) - 1})
           : eastl::make_pair(eastl::string{}, eastl::string{path, path_len});
}

struct StcodeBuildDirs
{
  eastl::string root;
  eastl::string location;
  eastl::string cache;
  eastl::string outDir;
};

static StcodeBuildDirs generate_dirs_with_provided_root(const char *engine_root, const char *out_dir,
  const StcodeCompilationDirs &stcode_dirs)
{
  const eastl::string cwd = get_cwd();

  auto toAbs = [&cwd](const char *src) {
    eastl::string res{src};
    if (!path_is_abs(src))
      res = cwd + "/" + res;
    dd_simplify_fname_c(res.data());
    res.resize(strlen(res.c_str()));
    if (res.back() == '/' && res.size() > 0)
      res.pop_back();
    return res;
  };

  auto tracebackPathFrom = [](const char *from) {
    int dirCount = 0;
    for (const char *p = from; p; p = strchr(p, '/'))
    {
      ++dirCount;
      ++p;
    }

    constexpr char UNIT[] = "../";
    constexpr size_t UNIT_LEN = sizeof(UNIT) - 1;
    eastl::string res{};
    res.resize(UNIT_LEN * dirCount);
    for (int i = 0; i < dirCount; ++i)
      memcpy(res.data() + UNIT_LEN * i, UNIT, UNIT_LEN);

    res.pop_back();
    return res;
  };

  auto makeRelPath = [&](const char *from, const char *to) {
    const char *pf = from, *pt = to;
    for (; *pf && *pt && *pf == *pt; ++pf, ++pt)
      ;

    if (*pf == '\0' && *pt == '\0')
      return eastl::string{"./"};
    else if (*pf == '\0' && *pt == '/')
      return eastl::string{pt + 1};
    else if (*pf == '/' && *pt == '\0')
      return tracebackPathFrom(pf + 1);
    else
    {
      do
      {
        --pf, --pt;
      } while (*pf != '/' && *pt != '/');
      return tracebackPathFrom(pf + 1) + "/" + eastl::string{pt + 1};
    }
  };

  const eastl::string outDirAbs = toAbs(out_dir);
  const eastl::string engineRootAbs = toAbs(engine_root);
  const eastl::string stcodeDirAbs = toAbs(stcode_dirs.stcodeDir.c_str());
  const eastl::string stcodeCacheDirAbs = toAbs(stcode_dirs.stcodeCompilationCacheDirUnmangled.c_str());

  StcodeBuildDirs res{};
  res.root = makeRelPath(cwd.c_str(), engineRootAbs.c_str());
  res.location = makeRelPath(engineRootAbs.c_str(), stcodeDirAbs.c_str());
  res.cache = makeRelPath(engineRootAbs.c_str(), stcodeCacheDirAbs.c_str());
  res.outDir = makeRelPath(engineRootAbs.c_str(), outDirAbs.c_str());
  return res;
}

static StcodeBuildDirs generate_dirs_with_inferred_root_from_rel_path(const char *out_dir, const StcodeCompilationDirs &stcode_dirs)
{
  const char *stcodeDir = stcode_dirs.stcodeDir.c_str();

  sh_debug(SHLOG_NORMAL,
    "[WARNING] engineRootDir var not found in blk, trying to generate stcode compilation paths from output path (%s). Note that "
    "this path must be relative to cwd and passing through engine root, or the build will fail!",
    stcodeDir);

  if (path_is_abs(stcodeDir))
  {
    sh_debug(SHLOG_FATAL, "output path (%s) can not be absolute when inferring root path", stcodeDir);
    return {};
  }

  eastl::string speculatedRelRoot = build_root_rel_path(speculate_root_depth_from_path(stcodeDir));
  return generate_dirs_with_provided_root(speculatedRelRoot.c_str(), out_dir, stcode_dirs);
}

#if !(_CROSS_TARGET_C1 | _CROSS_TARGET_C2)
static eastl::string make_pdb_path(const char *out_dir, const char *lib_name)
{
  constexpr char DEBINFO_EXT[] =
#if _TARGET_PC_WIN
    ".pdb"
#elif _TARGET_PC_LINUX
    ".so.debuginfo"
#else // _TARGET_PC_MACOSX
    ".dSYM"
#endif
    ;
  return eastl::string{out_dir} + "/" + eastl::string{lib_name} + config_to_mangled_suffix(shc::config().cppStcodeCompConfig) +
         DEBINFO_EXT;
}
#endif

static eastl::string make_zip_path(const char *out_dir, const char *lib_name)
{
  return eastl::string{out_dir} + "/" + eastl::string{lib_name} + config_to_mangled_suffix(shc::config().cppStcodeCompConfig) +
         ".debug.zip";
}

static void save_debug_info_and_sources_to_zip(const char *out_dir, const char *lib_name, const char *stcode_dir,
  const char *root_rel_path)
{
  auto command = string_f("python3 %s/prog/tools/ShaderCompiler2/make_cppstcode_debuginfo_zip.py %s d:%s", root_rel_path,
    make_zip_path(out_dir, lib_name).c_str(), stcode_dir);
#if !(_CROSS_TARGET_C1 | _CROSS_TARGET_C2)
  command += " f:";
  command += make_pdb_path(out_dir, lib_name);
#endif
  if (system(command.c_str()) != 0)
    sh_debug(SHLOG_WARNING, "Failed to zip cppstcode sources and debug info");
}

static void cleanup_after_stcode_compilation(const char *out_dir, const char *lib_name)
{
  G_UNUSED(out_dir);
  G_UNUSED(lib_name);

#if !(_CROSS_TARGET_C1 | _CROSS_TARGET_C2)
#if _CROSS_TARGET_SPIRV
  if (shc::config().cppStcodeDeleteDebugInfo && shc::config().usePcToken)
#else
  if (shc::config().cppStcodeDeleteDebugInfo)
#endif
  {
    dd_erase(make_pdb_path(out_dir, lib_name).c_str());
  }
#endif
}

dag::Expected<Tab<proc::ProcessTask>, StcodeMakeTaskError> make_stcode_compilation_tasks(const char *out_dir, const char *lib_name,
  const ShCompilationInfo &comp)
{
  RET_IF_SHOULD_NOT_COMPILE(dag::Unexpected(StcodeMakeTaskError::DISABLED));

  const auto &[stcodeDir, stcodeDirCacheUnmangled] = comp.stcodeDirs();

  // Calculate root path, stcode path relative to root and output dir relative to root
  const char *engineRoot = shc::config().engineRootDir.empty() ? nullptr : shc::config().engineRootDir.c_str();
  auto [rootRelPath, stcodeRelPath, stcodeCacheRelPath, outDirRelPath] =
    engineRoot ? generate_dirs_with_provided_root(engineRoot, out_dir, comp.stcodeDirs())
               : generate_dirs_with_inferred_root_from_rel_path(out_dir, comp.stcodeDirs());

  eastl::string sourcesList;

  if (shc::config().cppStcodeUnityBuild)
    sourcesList = "";
  else
  {
    StcodeBuilder strBuilder{};
    dag::VectorSet<eastl::string> requiredSources{};
    for (const String &shname : comp.sources())
    {
      eastl::string srcFileName = get_cpp_filename_from_source_name(shname.c_str(), shname.length());
      eastl::string filePath = stcodeDir + "/" + srcFileName;
      if (dd_file_exist(filePath.c_str()))
      {
        strBuilder.emplaceBack(srcFileName + "\n");
        requiredSources.insert(eastl::move(filePath));
      }
    }

    sourcesList = strBuilder.release();

    requiredSources.insert(stcodeDir + "/stcode_main.stcode.gen.cpp");
    requiredSources.insert(stcodeDir + "/glob_shadervars.stcode.gen.cpp");
    requiredSources.insert(stcodeDir + "/glob_refined_block.stcode.gen.cpp");

    // Cleanup stale files
    for (const alefind_t &ff : dd_find_iterator((stcodeDir + "/*.stcode.gen.cpp").c_str(), DA_FILE))
    {
      const eastl::string fullPath = stcodeDir + "/" + ff.name;
      if (requiredSources.find(fullPath) == requiredSources.end())
        dd_erase(fullPath.c_str());
    }
  }

  // Check version file
  bool versionsMatch = false;
  int ver = -1;

  {
    eastl::string versionFilePath = stcodeDir + "/" + STCODE_VER_FILE_NAME;
    file_ptr_t vf = df_open(versionFilePath.c_str(), DF_READ);
    if (vf)
    {
      char buf[128];
      int charsRead = df_read(vf, buf, sizeof(buf));
      if (charsRead < sizeof(buf))
      {
        buf[charsRead] = '\0';
        bool ok = semutils::try_int_number(buf, ver);
        if (ok && ver == CPP_STCODE_COMMON_VER)
          versionsMatch = true;
      }
      df_close(vf);
    }

    if (!versionsMatch)
    {
      vf = df_open(versionFilePath.c_str(), DF_WRITE | DF_CREATE);
      df_printf(vf, "%d", CPP_STCODE_COMMON_VER);
      df_close(vf);
    }
  }

  if (!versionsMatch)
  {
    sh_debug(SHLOG_NORMAL,
      "Cpp stcode versions do not match (ver=%d in compilation cache, ver=%d in compiler binary), recompiling generated code", ver,
      CPP_STCODE_COMMON_VER);
  }

  // The library's CMake project (built by prog/cmake/scripts/build_stcode.cmake) and the stamp of this generation
  constexpr char cmakeListsTemplate[] =
#include "_stcodeTemplates/CMakeLists.txt.fmt"
    ;
  const char *routineVisibility = shc::config().cppStcodeUnityBuild ? "static" : "extern";
  write_file_if_changed((stcodeDir + "/CMakeLists.txt").c_str(),
    eastl::string{eastl::string::CtorSprintf{}, cmakeListsTemplate, routineVisibility});
  write_file_if_changed((stcodeDir + "/stcode_files.cmake").c_str(),
    eastl::string{eastl::string::CtorSprintf{}, "set(FILES\n  stcode_main.stcode.gen.cpp\n%s)\n", sourcesList.c_str()});
  const eastl::string stamp = make_header_from_blk_hash<STAMP_HEADER_LEN, STAMP_HEADER_FMT>(comp.targetBlkHash());
  write_file((stcodeDir + "/stcode.stamp").c_str(), stamp.c_str(), stamp.length());

  if (shc::config().cppStcodeNoBuild)
    return dag::Unexpected(StcodeMakeTaskError::DISABLED);

  auto requiredArchs = shc::config().cppStcodeArchs;
  if (requiredArchs.empty())
    requiredArchs.push_back(StcodeTargetArch::DEFAULT);

  Tab<proc::ProcessTask> tasks{};
  tasks.reserve(requiredArchs.size());

  for (StcodeTargetArch reqArch : requiredArchs)
  {

    StcodeTargetArch arch = StcodeTargetArch::DEFAULT;

#define SET_ARCH_WITH_DEF(default_) arch = (reqArch == StcodeTargetArch::DEFAULT ? default_ : reqArch)

#if _TARGET_PC_WIN

#if _CROSS_TARGET_SPIRV
    SET_ARCH_WITH_DEF(platform_switch(StcodeTargetArch::X86_64, StcodeTargetArch::ARM64_V8A, StcodeTargetArch::ARM64));
#else
    SET_ARCH_WITH_DEF(StcodeTargetArch::X86_64);
#endif

    const char *platform =
#if _CROSS_TARGET_DX12
      platform_switch<const char *>("windows", "xboxOne", "scarlett")
#elif _CROSS_TARGET_DX11
      "windows"
#elif _CROSS_TARGET_SPIRV
      platform_switch<const char *>("windows", "android", "nswitch")
#elif _CROSS_TARGET_C1

#elif _CROSS_TARGET_C2

#else
      "<invalid>"
#endif
      ;

#elif _TARGET_PC_LINUX | _TARGET_PC_MACOSX

#if _TARGET_PC_LINUX && !(_CROSS_TARGET_SPIRV || _CROSS_TARGET_EMPTY)
#error Only spirv should be compiled on linux
#elif _TARGET_PC_MACOSX && !(_CROSS_TARGET_METAL || _CROSS_TARGET_SPIRV || _CROSS_TARGET_EMPTY)
#error Only metal and spirv should be compiled on mac
#endif

#if _TARGET_PC_LINUX
    const char *platform = platform_switch<const char *>("linux", "android", "nswitch");
    SET_ARCH_WITH_DEF(platform_switch(StcodeTargetArch::X86_64, StcodeTargetArch::ARM64_V8A, StcodeTargetArch::ARM64));
#else
#if _CROSS_TARGET_METAL
    const char *platform = if_ios<const char *>("iOS", "macOS");
    SET_ARCH_WITH_DEF(if_ios(StcodeTargetArch::ARM64, StcodeTargetArch::X86_64));
#else
    const char *platform = "android";
    SET_ARCH_WITH_DEF(StcodeTargetArch::ARM64_V8A);
#endif
#endif

#endif

    G_ASSERT(platform);

    const char *config = config_to_build_name(shc::config().cppStcodeCompConfig);

    proc::ProcessTask task{};
    task.isExternal = true;

    struct CompilationCompletionCbPayload
    {
      eastl::string dynlibName;
      eastl::string outDir;
      eastl::string stcodeDir;
      eastl::string rootRelPath;
    };

    eastl::string concreteDynlibName{lib_name};
    if (!arch_and_platform_is_fixed_for_shaders())
    {
      concreteDynlibName += "-";
      concreteDynlibName += platform;
      concreteDynlibName += "-";
      concreteDynlibName += arch_name_for_dll_name(arch);
    }
    if (shc::config().cppStcodeCustomTag)
    {
      concreteDynlibName += "-";
      concreteDynlibName += shc::config().cppStcodeCustomTag;
    }

    const eastl::string payloadDynlibName = concreteDynlibName;
    // Pointer to fit fixed lambda size limit
    auto payload = eastl::make_unique<CompilationCompletionCbPayload>(eastl::move(concreteDynlibName), eastl::string{out_dir},
      comp.stcodeDirs().stcodeDir, rootRelPath);

    task.onSuccess = [payload = eastl::move(payload)] {
      if (shc::config().cppStcodeSaveDebugInfoAndSourcesToZip)
      {
        save_debug_info_and_sources_to_zip(payload->outDir.c_str(), payload->dynlibName.c_str(), payload->stcodeDir.c_str(),
          payload->rootRelPath.c_str());
      }
      cleanup_after_stcode_compilation(payload->outDir.c_str(), payload->dynlibName.c_str());
    };

#if _TARGET_PC_WIN || _TARGET_PC_LINUX || _TARGET_PC_MACOSX

    const char *buildArch = arch_name_for_build(arch);
    if (!buildArch)
    {
      sh_debug(SHLOG_ERROR, "Cpp stcode can't be built for arch %s", arch_name(arch));
      return dag::Unexpected(StcodeMakeTaskError::DISABLED);
    }
#if _TARGET_PC_WIN
    task.argv.emplace_back("C:\\windows\\system32\\cmd.exe"); // finds cmake in PATH
    task.argv.emplace_back("/c");
#endif
    task.argv.emplace_back("cmake");
    task.argv.push_back(string_f("-DSOURCE_DIR=%s", stcodeDir.c_str()));
    task.argv.push_back(string_f("-DBINARY_DIR=%s/build-%s-%s", stcodeDir.c_str(), platform, buildArch));
    task.argv.push_back(string_f("-DPLATFORM=%s", platform));
    task.argv.push_back(string_f("-DARCH=%s", buildArch));
    task.argv.push_back(string_f("-DCONFIG=%s", config));
    task.argv.push_back(string_f("-DNAME=%s", payloadDynlibName.c_str()));
    task.argv.push_back(string_f("-DOUTPUT_DIR=%s", out_dir));
    if (!versionsMatch)
      task.argv.emplace_back("-DCLEAN=ON");
    task.argv.emplace_back("-P");
    task.argv.push_back(string_f("%s/prog/cmake/scripts/build_stcode.cmake", rootRelPath.c_str()));

#else // Stub

    return dag::Unexpected(StcodeMakeTaskError::DISABLED);

#endif

#undef VERIFY_AND_SET_ARCH
#undef SET_ARCH_WITH_DEF

    tasks.emplace_back(eastl::move(task));
  }

  return eastl::move(tasks);
}
