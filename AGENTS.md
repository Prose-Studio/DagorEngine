# AGENTS.md (Dagor Engine fork)

Guidance for coding agents working in this engine checkout (Prose-Studio fork; the upstream revision is in
`DagorEngine.rev.txt`). Game projects live outside it (e.g. `../Projects/Oyasumi`) and point at it through
`engineRoot` in their `application.blk`. Each game has its own `AGENTS.md`. Docs: `_docs/source` (getting-started,
api-references, assets, dagor-tools).

## Ground rules
- The upstream Dagor docs and APIs are not guaranteed to match this fork. Verify against the code here before relying
  on an API.
- Engine changes made for a game must stay generic and small. Explain why in the commit message. Do not mix
  game-specific code into the engine.
- This repo may hold the owner's uncommitted work: never commit, stash, reset or reformat files you did not change.

## Build
- Toolchain setup, once: `python dagor.py devtools <dir>` (jam 2.5-G8, clang 21.1.8 on Windows x64, VS 2022 SDKs;
  writes `prog/platform.jam`).
- Tools (CDK): `python dagor.py build project:dagorTools code`, output to `tools/dagor_cdk/<platform>-<arch>`.
- A single jam target: run `jam` in the folder holding its `jamfile` (e.g. `prog/engine/tests/osApiWrappers`).
  Intermediate files go to `_output/`.
- New game project: `python dagor.py new --template sp-3d|mp-3d|sp-2d|mp-2d --name <Name>` (layers in `templates/`).
  `relink` repoints a project at this checkout.
- Defaults to know: game code builds with `-fp:fast` / `-ffast-math` (`prog/_jBuild/defaults.jam:155`,
  `prog/_jBuild/*/clang-sets.jam`). Only tools force `-fp:precise` (`prog/tools/tools_setup.jam`).
- Verified hosts: Windows x64 only. Linux and macOS scripts exist but have not been run on this fork.

## Tests
- C++: Catch2 console exes (`prog/3rdPartyLibs/catch2`), one jamfile per suite, e.g.
  `prog/engine/tests/osApiWrappers/jamfile` → `_output/dagorUnitTests/<target>-dev.exe`.
- daScript: `prog/1stPartyLibs/daScript/dastest` needs the `das-64` runner (`prog/1stPartyLibs/daScript/utils/daScript/jamfile`),
  which is not built by default. Nothing handles a `-das_test` game flag.

## ECS and scripting patterns
- C++ ES: `*ES.cpp.inl` with `ECS_TAG`, `ECS_ON_EVENT`, `ECS_BEFORE/AFTER`, generated into `.gen.es.cpp` by
  `GenESSourceFile` (`prog/_jBuild/jCommonRules.jam`).
- das modules: a `das::Module` subclass, `addExtern<DAS_BIND_FUN(...)>`, `REGISTER_MODULE_IN_NAMESPACE`. A game pulls
  its modules in through `pull_game_das()`, and the das AOT target must compile them too.
- Update order per frame and fixed vs variable act rate: `prog/daNetGame/main/app.cpp` (`actRate` setting, line 829).

## Known gaps (as of 2026-10-14)
- Input: all pads merge into one composite device, and daInput is single-user (`prog/dagorInclude/drv/hid/dag_hiComposite.h`,
  `prog/gameLibs/publicInclude/daInput/input_api.h`).
- Assets: there is no FBX/glTF importer. Skinned `.dag` and `.a2d` come from the 3ds Max plugin (`prog/tools/maxplug`)
  only. dag4blend exports static geometry.
- daNetGame does not send `UpdateAnimcharEvent`; the game must drive animchar updates.
- The only CI workflow builds docs (`.github/workflows/documentation.yaml`).
