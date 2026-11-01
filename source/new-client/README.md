# The new client - source

The new client is a game client for a DAoC server (OpenDAoC-based, 1.65 rules), built in Godot 4.7 (.NET). It
speaks the original DAoC network protocol (game client version 1.127) to any compatible server, so it needs no
server changes: everything it shows is decoded from packets the server already sends.

## Layout

| Path | What it is |
|---|---|
| `godot/` | The Godot project. `game/` is all client code (GDScript, plus the network client in C#: `game/net/DaocClient.cs`). `game/net/server.gd` and `game/net/server_world.gd` turn the server's packets into the game world and interface. |
| `godot/tests/` | Headless checks and debug probes (`tests/load_check.gd` compiles scripts with the autoloads present). |
| `godot/tools/` | Content maintenance scripts run inside Godot (`pack_scenes.gd` packs converted models into `.scn` files). |
| `pipeline/` | The Python content pipeline: it reads the original DAoC client's files (zones, NIF models, textures, sounds, interface art, game data) and writes the converted content into `godot/content`. `nif_static.py` / `nif_character.py` read NetImmerse models (`spec/nif.xml` from NifTools). |
| `tools/build_csharp.ps1` | Windows-only: builds the C# network client via PowerShell. |
| `tools/build_csharp.py` | Cross-platform equivalent of the above; needs the .NET SDK's `dotnet` on PATH (or `DOTNET=/path/to/dotnet`). |
| `tools/run_dev.py` | Launches the client from source against an already-running server, for local testing on any platform. |

The repository holds the source only. The converted content (`godot/content`, about 33 GB) is not included; it
has to come from a build of the matching content pipeline, or be copied/symlinked in from an existing install
that was built from the same upstream version this source is pinned to.

## Running from source

1. Install the .NET 10 SDK and a Godot 4.7.2 (.NET/mono) build for your platform.
2. Get `godot/content` into place (see above). `godot/content/.gdignore` must stay: Godot must not import the
   content folder.
3. Get `tools/godot_net/GodotSharp` into place: a copy or symlink of a matching Godot 4.7.2 (.NET) build's own
   `Contents/Resources/GodotSharp` (macOS app bundle) or equivalent `GodotSharp` folder (Windows/Linux) — this is
   the offline NuGet source `godot/nuget.config` points at for building the C# project.
4. Build the network client: `python3 tools/build_csharp.py` (cross-platform) or `tools\build_csharp.ps1`
   (Windows). Run it again after every change to a `.cs` file; starting the game with `--path` does not compile
   C#.
5. Start a server, then run:
   `python3 tools/run_dev.py --godot /path/to/Godot(.app) --server=<host>` (prompts for account/password locally)
   — or invoke the Godot build directly:
   `Godot --path godot -- --server=<host> --account=<name> --password=<password>`.

## Developer mode

The debug text (Ctrl+F12), the bot inspector (Ctrl+F11) and the Ctrl+F1..F11 test keys work only when
`godot/dev_mode.txt` exists or the game is started with `--dev` (`game/ui/boot_settings.gd`). Release packages
never include that file.

## The content pipeline

The pipeline needs Python 3.10+ (`pipeline/requirements-full.txt`), Real-ESRGAN for the 4x texture upscale
(`tools/realesrgan/realesrgan-ncnn-vulkan.exe` with its `models` folder), and the original DAoC client's files (set `DAOC_CLIENT` to the client's folder; the 0.36 release
content was built from the 0.36b client, so the Sluaghbinder's custom effects are included). Each `build_*.py`
script says at its top what it builds and how to run it. A full rebuild takes many hours. After a model or effect
rebuild, repack the scenes:
`Godot --headless --path godot -s res://tools/pack_scenes.gd -- --force res://content/monsters/effects`.

## Packaging a standalone build

This fork doesn't carry the release-packaging tooling upstream used (that built a full downloadable game
package, not just the client). To produce a standalone build, export the project in the Godot editor for your
target platform (Project > Export), with the matching export templates for Godot 4.7.2 installed, and ship the
exported binary alongside a populated `content/` folder. Make sure `dev_mode.txt` is not present before
exporting a build meant to leave your machine.
