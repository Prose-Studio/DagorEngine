options gen2
require ecs
require DagorEditor
require danetlibs/test_harness/scenario

// ctest --preset <host>-client -R starter_game.editor
// The embedded editor (F12, outside Rel builds) opens over the game and closes again; its daRg UI, the UI fonts and the
// overlay UI script load without errors (an error fails the test).

[ecs_test]
def the_embedded_editor_opens_and_closes(t : T?) {
  advance_frames(10)
  console_command("daEd4.open 1") // what F12 does
  advance_frames(30)
  t |> success(is_editor_activated(), "daEd4.open 1 did not open the editor")
  console_command("daEd4.open 0")
  advance_frames(10)
  t |> success(!is_editor_activated(), "daEd4.open 0 did not close the editor")
}
