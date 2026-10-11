# daScript's standard library scripts compiled ahead of time (DAGOR_DAS_AOT), which 1stPartyLibs/daScript links then
set(das algorithm apply apply_in_context array_boost assert_once ast_boost constant_expression contracts cpp_bind dap
  debug debug_eval defer enum_trait functional if_not_null instance_function is_local jobque_boost json json_boost lint
  lint_everything lpipe macro_boost match math_bits regex regex_boost remove_call_args safe_addr sort_boost static_let
  strings_boost stub templates templates_boost typemacro_boost utf8_utils)
list(TRANSFORM das APPEND .das)
dagor_add_library(
  PRIVATE_INCLUDES ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  DAS_AOT ${das} DAS_AOT_PULL daslib_DAS_pull_AOT
  LICENSE_FILES ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/LICENSE
)
