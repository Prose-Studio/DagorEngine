options gen2
require app
require ecs
require DngNet
require DagorSystem
require DagorDataBlock
require strings

// the port the dedicated server listens on (game/server.cmd: -listen:0.0.0.0:2992), and -connect:<host> joins
let DEFAULT_PORT = 2992

// Once the game is up: a client started with -connect:<host>[:<port>] joins that dedicated server, which gives it the
// scene. The dedicated server, or a client without -connect (a local game: its own server), loads its scene:
// -scene:<path>, else settings.blk scene:t=
[es(on_event=EventOnGameAppStarted)]
def game_start_es(evt : Event) {
  let server = dgs_get_argv("connect")
  if (!empty(server) && !is_dedicated()) {
    var urls : array<string>
    urls |> push(find(server, ":") >= 0 ? server : "{server}:{DEFAULT_PORT}")
    print("connecting to {urls[0]}")
    connect_to_session(urls)
    return
  }
  var scene = dgs_get_argv("scene")
  if (empty(scene)) {
    scene = dgs_get_settings() |> datablock_getStr("scene", "")
  }
  print("starting scene {scene}")
  switch_scene(scene)
}
