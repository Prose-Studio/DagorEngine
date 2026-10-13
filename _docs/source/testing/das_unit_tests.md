# daScript Unit Tests

Pure daScript code (logic that doesn't need the running game) is tested with daScript's own framework, `dastest`
(`prog/1stPartyLibs/daScript/dastest`), in the engine's das interpreter (the `das` program of the tree, built with the tests).

```text
options gen2
require dastest/testing_boost public
require my_game/lib/damage

[test]
def damage_is_reduced_by_armor(t : T?) {
  t |> equal(apply_armor(100, 25), 75)
  t |> run("never negative") <| @(t : T?) {
    t |> success(apply_armor(10, 50) >= 0)
  }
}
```

The `T` API: `equal`, `strictEqual`, `numericEqual`, `success`, `failure`, `accept`, `run` (sub tests), `skip`,
`log`, `error`, `fatal` (`t->fatal(...)`), `skipNow`.

## Declaring the tests

```cmake
dagor_add_das_test(myGame.logic TAGS my_game
  PATHS ../scripts/my_game               # dirs or files with tests
  PROJECT ../scripts/tests.das_project   # optional: module paths for require
  ISOLATED)                              # optional: every test file in its own process
```

The engine registers the daScript language suite as `daScript.suite`; `ctest -R daScript -V` runs it with its output.
