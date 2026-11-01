#!/usr/bin/env python3
"""Cross-platform equivalent of build_csharp.ps1: rebuilds the game's C# part (godot/MMOEngine.csproj)
only when a .cs file is newer than what was last built. Needs the .NET SDK on PATH (or set
DOTNET env var to its full path) and godot/tools/godot_net/GodotSharp/Tools/nupkgs populated
(a symlink or copy of the matching Godot .NET build's own GodotSharp/Tools/nupkgs folder; see
../README.md).

Usage: python3 build_csharp.py
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # source/new-client
GODOT_DIR = ROOT / "godot"
DLL = GODOT_DIR / ".godot" / "mono" / "temp" / "bin" / "Debug" / "MMOEngine.dll"


def newest_cs_mtime() -> float:
    newest = 0.0
    for path in GODOT_DIR.rglob("*.cs"):
        parts = path.parts
        if ".godot" in parts or "obj" in parts:
            continue
        mtime = path.stat().st_mtime
        if mtime > newest:
            newest = mtime
    return newest


def main() -> int:
    dotnet = os.environ.get("DOTNET") or shutil.which("dotnet")
    if not dotnet:
        print("dotnet not found on PATH; install the .NET SDK or set DOTNET=/path/to/dotnet", file=sys.stderr)
        return 1

    if DLL.is_file() and newest_cs_mtime() <= DLL.stat().st_mtime:
        print("C# part up to date.")
        return 0

    print("Building the C# part...")
    result = subprocess.run([dotnet, "build", str(GODOT_DIR / "MMOEngine.csproj"), "-c", "Debug", "-v", "q", "--nologo"])
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
