#!/usr/bin/env python3
"""Shared helpers for dumbass-tree CLI scripts.

Intentionally small and dependency-free.
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


def _shlex_join(argv: Sequence[str]) -> str:
    """Best-effort shell-ish join for printing."""
    join = getattr(shlex, "join", None)
    if join is not None:
        return join(list(argv))
    return " ".join(shlex.quote(a) for a in argv)


def die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def warn(msg: str) -> None:
    print(f"warn: {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(msg)


def require_root() -> None:
    euid = os.geteuid() if hasattr(os, "geteuid") else 1
    if euid == 0:
        return
    die("this operation requires root (try: sudo ...)")


def require_cmd(cmd: str) -> str:
    path = shutil.which(cmd)
    if not path:
        die(f"required command not found in PATH: {cmd}")
    return path


def require_cmds(cmds: Iterable[str]) -> None:
    for c in cmds:
        require_cmd(c)


def confirm_or_exit(
    *,
    yes: bool,
    dry_run: bool,
    prompt: str,
    reason: str,
    alternatives: Sequence[str] = (),
    typed: str | None = None,
) -> None:
    """Require --yes or an interactive confirmation prompt.

    This is the core safety valve used across the dumbass-tree tools.

    Behavior:
    - If dry_run is True, this is a no-op (nothing will be changed).
    - If yes is True, proceed without prompting.
    - If stdin is not a TTY (non-interactive), require --yes.
    - Otherwise, prompt the user to confirm.

    typed:
      If provided, the user must type this exact token to proceed.
      Example: typed=f"DESTROY {pool}".
    """
    if dry_run:
        return
    if yes:
        return

    # Non-interactive: force explicit --yes so scripts don't hang or do scary things.
    if not sys.stdin.isatty():
        msg = (
            f"{prompt}\n\n"
            f"You need to pass --yes or run interactively because: {reason}"
        )
        if alternatives:
            msg += "\n\nAlternatives:\n" + "\n".join(f"  - {a}" for a in alternatives)
        die(msg)

    # Interactive: show context + require confirmation.
    print(prompt, file=sys.stderr)
    print(f"Reason: {reason}", file=sys.stderr)
    if alternatives:
        print("Alternatives:", file=sys.stderr)
        for a in alternatives:
            print(f"  - {a}", file=sys.stderr)

    if typed:
        ans = input(f"Type {typed!r} to continue (or anything else to abort): ").strip()
        if ans != typed:
            die("aborted")
        return

    ans = input('Type "yes" to continue (or anything else to abort): ').strip().lower()
    if ans != "yes":
        die("aborted")




def confirm_two_tier_or_exit(
    *,
    yes: bool,
    dry_run: bool,
    prompt: str,
    reason: str,
    alternatives: Sequence[str] = (),
    typed: str,
    second_prompt: str | None = None,
) -> None:
    """Two-tier confirmation for *really* dangerous operations.

    Tier 1: "are you sure?" (y/N)
    Tier 2: "no no, really" (type an exact phrase)

    This is intentionally annoying. That's the point.
    """

    if dry_run or yes:
        return

    # Non-interactive: require explicit --yes.
    if not sys.stdin.isatty():
        msg = (
            f"You need to pass --yes or run interactively because: {reason}"
        )
        if alternatives:
            msg += "\n\nAlternatives:\n" + "\n".join(f"  - {a}" for a in alternatives)
        die(msg)

    # Tier 1
    print(prompt, file=sys.stderr)
    print(f"Reason: {reason}", file=sys.stderr)
    if alternatives:
        print("Alternatives:", file=sys.stderr)
        for a in alternatives:
            print(f"  - {a}", file=sys.stderr)

    ans = input("Continue? [y/N]: ").strip().lower()
    if ans not in ("y", "yes"):
        die("aborted")

    # Tier 2
    banner = second_prompt or (
        "\n\N{police cars revolving light}\N{police cars revolving light}\N{police cars revolving light}  DANGER ZONE  \N{police cars revolving light}\N{police cars revolving light}\N{police cars revolving light}\n"
        "This WILL permanently destroy or overwrite data.\n"
        "If you are not 100% sure, hit Ctrl+C or type anything other than the magic phrase.\n"
    )
    print(banner, file=sys.stderr)
    ans2 = input(f"Type {typed!r} to continue (or anything else to abort): ").strip()
    if ans2 != typed:
        die("aborted")


@dataclass
class RunResult:
    argv: list[str]
    returncode: int
    stdout: str = ""
    stderr: str = ""


def run(
    argv: Sequence[str],
    *,
    dry_run: bool = False,
    verbose: int = 0,
    check: bool = True,
    capture: bool = False,
    env: Mapping[str, str] | None = None,
) -> RunResult:
    """Run a command.

    - dry_run: prints command, does not execute
    - verbose: prints command before executing when verbose > 0
    - capture: capture stdout/stderr instead of inheriting terminal
    """
    cmd = list(argv)
    if dry_run or verbose > 0:
        prefix = "+ " if dry_run else "$ "
        print(prefix + _shlex_join(cmd), file=sys.stderr)

    if dry_run:
        return RunResult(argv=cmd, returncode=0, stdout="", stderr="")

    try:
        if capture:
            cp = subprocess.run(
                cmd,
                env=dict(os.environ, **(env or {})),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if check and cp.returncode != 0:
                raise subprocess.CalledProcessError(
                    cp.returncode, cmd, output=cp.stdout, stderr=cp.stderr
                )
            return RunResult(argv=cmd, returncode=cp.returncode, stdout=cp.stdout, stderr=cp.stderr)
        else:
            cp = subprocess.run(cmd, env=dict(os.environ, **(env or {})))
            if check and cp.returncode != 0:
                raise subprocess.CalledProcessError(cp.returncode, cmd)
            return RunResult(argv=cmd, returncode=cp.returncode)
    except FileNotFoundError:
        die(f"command not found: {cmd[0]}")
    except subprocess.CalledProcessError as e:
        # Provide nicer output; keep stderr/stdout if captured
        if hasattr(e, "stderr") and e.stderr:
            sys.stderr.write(e.stderr)
        if hasattr(e, "stdout") and e.stdout:
            sys.stdout.write(e.stdout)
        die(f"command failed with exit code {e.returncode}: {cmd[0]}", code=e.returncode)


def parse_kib_size(size: str) -> int:
    """Parse sizes like '2048kB', '2M', '1G' into KiB."""
    s = size.strip().lower()
    # sysfs hugepages directory names use kB (powers of 1024) semantics in practice.
    if s.endswith("kb"):
        return int(s[:-2])
    mult = 1
    if s.endswith("k"):
        mult = 1
        s = s[:-1]
    elif s.endswith("m"):
        mult = 1024
        s = s[:-1]
    elif s.endswith("g"):
        mult = 1024 * 1024
        s = s[:-1]
    try:
        base = int(s)
    except ValueError:
        die(f"invalid size: {size} (expected e.g. 2M, 1G, 2048kB)")
    return base * mult


def format_size_kib(kib: int) -> str:
    if kib % (1024 * 1024) == 0:
        return f"{kib // (1024 * 1024)}G"
    if kib % 1024 == 0:
        return f"{kib // 1024}M"
    return f"{kib}K"
