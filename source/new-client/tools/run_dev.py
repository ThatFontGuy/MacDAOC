#!/usr/bin/env python3
"""Launches the new client from source against a already-running DAoC server, for local testing.
Does not install or build anything itself: run build_csharp.py first after any .cs change, and
point --godot at a Godot 4.7.2 (.NET/mono) build you already have (the editor executable, or a
macOS Godot.app bundle).

Prompts for the account name and password locally (nothing is stored or printed back) -
--server alone makes the client skip its own login screen straight to an auto-login attempt
(game/login_screen.gd has no field to type into in that mode), so credentials have to be passed
on the command line, same as upstream's own launcher does it.

Usage:
  python3 run_dev.py --godot /path/to/Godot.app --server 192.168.1.69 [--custom-class-off]
  python3 run_dev.py --godot /path/to/godot.linux.x86_64 --server 192.168.1.69
"""
import argparse
import getpass
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # source/new-client
GODOT_PROJECT = ROOT / "godot"
NEW_PORT = 10300


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--godot", required=True, help="path to a Godot 4.7.2 (.NET) build: the editor binary, or a macOS .app bundle")
    parser.add_argument("--server", required=True, help="server address (host or host:port; default port 10300)")
    parser.add_argument("--account", help="account name (prompted if omitted)")
    parser.add_argument("--custom-class-off", action="store_true", help="hide the Sluaghbinder at character creation, matching a server with classes/enable_sluaghbinder = False")
    parser.add_argument("--dotnet-root", help="DOTNET_ROOT to export to the child process, if your dotnet install isn't the system default")
    args = parser.parse_args()

    if not GODOT_PROJECT.is_dir() or not (GODOT_PROJECT / "project.godot").is_file():
        print(f"no Godot project found at {GODOT_PROJECT}", file=sys.stderr)
        return 1

    godot_path = Path(args.godot).expanduser().resolve()
    if not godot_path.exists():
        print(f"Godot build not found at {godot_path}", file=sys.stderr)
        return 1

    account = args.account or input("Account name (letters/numbers only - created on first login): ").strip()
    if not account:
        print("an account name is required", file=sys.stderr)
        return 1
    password = getpass.getpass("Password: ")
    if not password:
        print("a password is required", file=sys.stderr)
        return 1

    server = args.server if ":" in args.server else f"{args.server}:{NEW_PORT}"
    game_args = [f"--server={server}", f"--account={account}", f"--password={password}"]
    if args.custom_class_off:
        game_args.append("--custom-class=off")

    env = os.environ.copy()
    if args.dotnet_root:
        env["DOTNET_ROOT"] = args.dotnet_root

    if godot_path.suffix == ".app":
        # macOS app bundle: launch through `open` so it runs as a normal GUI app, not attached
        # to this terminal.
        cmd = ["/usr/bin/open", "-n", "-W", str(godot_path)]
        if args.dotnet_root:
            cmd += ["--env", f"DOTNET_ROOT={args.dotnet_root}"]
        cmd += ["--args", "--path", str(GODOT_PROJECT), "--", *game_args]
    else:
        cmd = [str(godot_path), "--path", str(GODOT_PROJECT), "--", *game_args]

    print(f"launching the new client, connecting to {server} as {account} ...")
    return subprocess.run(cmd, env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main())
