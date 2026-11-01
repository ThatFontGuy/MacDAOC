# MacDAOC — instructions for AI assistants and developers

This file is also loaded by Claude Code as `CLAUDE.md`.

## What this is

MacDAOC is a personal fork of [shadowofze/OfflineDAoC](https://github.com/shadowofze/OfflineDAoC)
("Offline DAoC"), trimmed down to keep only its **new client**: a Dark Age of Camelot (1.65 rules)
game client built in the Godot 4 (.NET) engine. It speaks the original DAoC network protocol (game
client version 1.127) to any compatible 1.65 server; the owner runs their own server separately, so
the game server, bot AI, launcher and release tooling from upstream are deliberately **not** part of
this repository, and never should be added back wholesale.

The goal of this fork is to produce a **macOS port** of the client. It is currently Windows-only in
practice: the C# build step is a PowerShell script (`source/new-client/tools/build_csharp.ps1`), and
the run instructions in [source/new-client/README.md](source/new-client/README.md) reference the
Windows `Godot_v4.7.2-stable_mono_win64.exe` binary. No macOS-specific code exists yet.

## Layout

| Path | What it is |
|---|---|
| `source/new-client` | The whole client: the Godot project (`godot/`) and the Python content pipeline (`pipeline/`) that converts the original DAoC client's files into Godot content. See its own [README](source/new-client/README.md). |
| `source/new-client/godot/game` | All client code: GDScript, plus the network client in C# (`net/DaocClient.cs`). |
| `source/new-client/godot/tools` | Content maintenance scripts run inside Godot (e.g. `pack_scenes.gd`). |
| `source/new-client/pipeline` | Reads the original client's zones, NIF models, textures, sounds, interface art and game data, and writes converted content into `godot/content` (not checked into Git — about 33 GB). |
| `docs/CLIENT-MODDING-GUIDE.txt` | File-format notes (catalog rules, item/model chains, NIF structure) for the original client's files that the pipeline converts. |

## Rules

- **Keep this repo client-only.** Don't pull in the upstream server, bot AI, launcher or release
  packaging tooling. If testing requires a server, that's the owner's separately run instance —
  never add server source or a bundled server here.
- **Protect credentials and saves.** Never commit `account.txt`, the new client's `save/` folder
  contents, logs, or any server connection details.
- **Don't edit stock converted content in place.** The pipeline's output under `godot/content` is
  derived from the original client's files; treat it as generated, not hand-edited. Private/custom
  additions follow the pattern in [docs/CLIENT-MODDING-GUIDE.txt](docs/CLIENT-MODDING-GUIDE.txt):
  new IDs, never overwriting stock models, skins or NIFs in place.
- **Don't start or deploy without permission.** Never start the client against a live server, or
  overwrite a running install, without asking first.
- **Build and test separately.** Deploy only tested outputs, with a backup of what you replace.
- **Be honest in reports.** Report automated/headless checks (`source/new-client/godot/tests`)
  separately from real in-client checks. Don't describe something as working in-game unless it's
  actually been verified against a running server.

## Useful facts

- **Item model chain:** `objects.csv` model ID → `items.csv` row → `items/<nif>`. Shields that carry
  an emblem take their base texture from a `pskins.csv` override. The pipeline's own NIF readers are
  `pipeline/nif_static.py` (static meshes) and `pipeline/nif_character.py` (characters).
- **Client art, spells and sounds:** read
  [docs/CLIENT-MODDING-GUIDE.txt](docs/CLIENT-MODDING-GUIDE.txt) before changing how models, meshes,
  skins, spell effects, icons or NPC sounds are converted or rendered. It lists the original client's
  catalog rules, confirmed and unconfirmed limits, and past mistakes.
- **Developer mode:** the debug text (Ctrl+F12), bot inspector (Ctrl+F11) and Ctrl+F1..F11 test keys
  work only when `godot/dev_mode.txt` exists or the game is started with `--dev`
  (`game/ui/boot_settings.gd`). Never commit `dev_mode.txt`.

The owner may customize this fork's rules further. These are safety defaults, not a ban on changes
the owner asks for.
