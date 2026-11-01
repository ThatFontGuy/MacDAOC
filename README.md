> **Disclaimer.** Dark Age of Camelot is the intellectual property of Electronic Arts and Broadsword
> Online Games. This project is not affiliated with, endorsed by, or connected to either company. The
> game client, textures, models and other assets it converts belong to them, and this project is built
> on top of that copyrighted work.
>
> This is a free, non-commercial fan project. It is not a product and it is not for sale. The client
> files it converts are the same publicly available ones every free shard uses; the work original to
> this repository is the new client's own code. Because the code is open source, the owner cannot
> control what forks or other people do with it.

# MacDAOC — a Godot 4 Dark Age of Camelot client

This repository is a personal fork of [shadowofze/OfflineDAoC](https://github.com/shadowofze/OfflineDAoC)
("Offline DAoC"), trimmed down to keep only its **new client**: a Dark Age of Camelot (1.65 rules) game
client built in the Godot 4 engine. Everything else from the upstream project (the game server, bot AI,
launcher, release tooling and the original Windows client) has been removed — this fork is not meant to
run its own server. It speaks the original DAoC network protocol (game client version 1.127), so it
works against any compatible 1.65 server.

The goal of this fork is to build a **macOS port** of the client, which is currently Windows-only in
practice (its build step is a PowerShell script, and it ships via a Windows-only launcher upstream).
No macOS-specific code exists yet.

## Where the code is

- [source/new-client](source/new-client): the whole client.
  - [source/new-client/godot](source/new-client/godot): the Godot project. `game/` is all client code
    (GDScript, plus the network client in C#: `game/net/DaocClient.cs`).
  - [source/new-client/pipeline](source/new-client/pipeline): the Python content pipeline that converts
    the original DAoC client's files (zones, NIF models, textures, sounds, interface art, game data)
    into the Godot project's `godot/content` folder (not checked into Git; see its own README).
  - [source/new-client/tools](source/new-client/tools): `build_csharp.ps1` builds the C# network
    client — Windows-only today, a good starting point for a macOS build step.
- [docs/CLIENT-MODDING-GUIDE.txt](docs/CLIENT-MODDING-GUIDE.txt): file-format notes (catalog rules,
  item/model chains, NIF structure) for the original client's files that the pipeline above converts.

See [source/new-client/README.md](source/new-client/README.md) for how to build and run it from source.

## For developers and AI assistants

[AGENTS.md](AGENTS.md) (also read by Claude as [CLAUDE.md](CLAUDE.md)) has the project rules for this
fork.

## Licensing

This project's own code is licensed under the **GNU General Public License v3.0** (see
[LICENSE](LICENSE)), inherited from the upstream OpenDAoC-based project this fork came from. See
[THIRD_PARTY.md](THIRD_PARTY.md) for the new client's own dependencies and their licenses. The
original game client is a binary dependency; this repository has only the new client's own source
code, not the original client's source or its converted content (which is not checked into Git).

## Upstream

The full project this was forked from, including the server, bots and original client support, is
[shadowofze/OfflineDAoC](https://github.com/shadowofze/OfflineDAoC). As of this fork, upstream's README
states the project is on hold and will not receive further updates.
