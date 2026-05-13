#!/usr/bin/env python3
"""
check-contrast.py — WCAG 2.x contrast ratio checker for CSS variable palettes.

Usage:
    check-contrast.py <file>              # auto-detect --bg, report vs --bg
    check-contrast.py <file> --bg <name>  # use a specific token as the base
    check-contrast.py <file> --pairs      # report ALL pairwise ratios
    check-contrast.py <file> --strict     # exit 1 if any non-muted token < 4.5:1

Reads CSS variable declarations (`--name: #hex`) from any text file
(CSS, HTML with embedded <style>, JSX, etc). Computes WCAG 2.x relative
luminance and contrast ratios using the official formula.

No network calls, no dependencies beyond the stdlib. Designed to run in
the frontend-design skill workflow before declaring a design done.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ANSI colors for terminal output
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

VAR_RE = re.compile(
    r"(--[a-zA-Z][a-zA-Z0-9_-]*)\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\))",
)

# Tokens that are EXPECTED to fail body-text contrast (hint/decorative text).
# Flagged as info, not failure, in --strict mode.
MUTED_TOKENS = {"muted", "rule", "hint", "border", "divider", "subtle", "ghost"}

# Tokens that represent alternate surfaces, not foreground text. Skipped from
# the 4.5:1 text-contrast check; instead checked at 3:1 for UI distinguishability.
SURFACE_TOKENS = {"bg", "background", "surface", "canvas", "panel", "card", "well", "shell"}


def parse_hex(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) == 4:  # #rgba shorthand
        s = "".join(c * 2 for c in s[:3])
    if len(s) == 8:  # #rrggbbaa — drop alpha
        s = s[:6]
    if len(s) != 6:
        raise ValueError(f"unrecognized hex color: {s}")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def parse_rgb(s: str) -> tuple[int, int, int]:
    nums = re.findall(r"[\d.]+", s)
    if len(nums) < 3:
        raise ValueError(f"unrecognized rgb: {s}")
    r, g, b = (float(n) for n in nums[:3])
    # supports rgb(0-255) or rgb(0-1) form rare; assume 0-255
    return int(r), int(g), int(b)


def to_rgb(value: str) -> tuple[int, int, int]:
    v = value.strip()
    if v.startswith("#"):
        return parse_hex(v)
    if v.lower().startswith(("rgb(", "rgba(")):
        return parse_rgb(v)
    raise ValueError(f"unsupported color: {value}")


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """WCAG 2.x relative luminance."""

    def channel(c: int) -> float:
        cs = c / 255.0
        return cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la = relative_luminance(a)
    lb = relative_luminance(b)
    lighter, darker = (la, lb) if la > lb else (lb, la)
    return (lighter + 0.05) / (darker + 0.05)


def grade(ratio: float) -> tuple[str, str]:
    """Return (label, ansi_color) for a contrast ratio."""
    if ratio >= 7.0:
        return ("AAA", GREEN)
    if ratio >= 4.5:
        return ("AA", GREEN)
    if ratio >= 3.0:
        return ("AA-Large", YELLOW)
    return ("FAIL", RED)


def extract_palette(text: str) -> dict[str, tuple[int, int, int]]:
    out: dict[str, tuple[int, int, int]] = {}
    for match in VAR_RE.finditer(text):
        name = match.group(1)
        raw = match.group(2)
        try:
            out[name] = to_rgb(raw)
        except ValueError:
            continue
    return out


def short_name(token: str) -> str:
    return token.lstrip("-")


def is_muted(token: str) -> bool:
    base = short_name(token).lower()
    return any(m in base for m in MUTED_TOKENS)


def is_surface(token: str) -> bool:
    base = short_name(token).lower()
    # match whole-word-ish: bg, bg-deep, surface, surface-2, canvas
    parts = re.split(r"[-_]", base)
    return any(p in SURFACE_TOKENS for p in parts)


def main() -> int:
    p = argparse.ArgumentParser(description="WCAG contrast checker for CSS variable palettes.")
    p.add_argument("file", help="CSS / HTML / JSX file containing --var declarations")
    p.add_argument("--bg", help="token name to use as base (default: auto-detect --bg or --background)")
    p.add_argument("--pairs", action="store_true", help="report ALL pairwise ratios")
    p.add_argument("--strict", action="store_true", help="exit 1 if any non-muted token fails 4.5:1 vs base")
    args = p.parse_args()

    src = Path(args.file)
    if not src.exists():
        print(f"{RED}file not found:{RESET} {src}", file=sys.stderr)
        return 2

    text = src.read_text(encoding="utf-8", errors="replace")
    palette = extract_palette(text)
    if not palette:
        print(f"{YELLOW}no CSS variables found in{RESET} {src}")
        return 0

    # decide base token
    base = args.bg
    if base and not base.startswith("--"):
        base = "--" + base
    if not base:
        for cand in ("--bg", "--background", "--surface", "--canvas", "--bg-deep"):
            if cand in palette:
                base = cand
                break
    if not base or base not in palette:
        print(f"{RED}no usable base token. pass --bg <name>.{RESET}", file=sys.stderr)
        print(f"available: {', '.join(palette)}", file=sys.stderr)
        return 2

    base_rgb = palette[base]
    print(f"{BOLD}palette{RESET}  {DIM}{src}{RESET}")
    print(f"{DIM}{'-' * 60}{RESET}")
    for name, rgb in palette.items():
        marker = f"{BOLD}<- base{RESET}" if name == base else ""
        print(f"  {name:<14} #{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}  Y={relative_luminance(rgb):.3f}  {marker}")

    print()
    print(f"{BOLD}contrast vs {base}{RESET}")
    print(f"{DIM}{'-' * 60}{RESET}")
    failures: list[tuple[str, float]] = []
    surface_warnings: list[tuple[str, float]] = []
    for name, rgb in palette.items():
        if name == base:
            continue
        ratio = contrast_ratio(rgb, base_rgb)
        label, color = grade(ratio)
        tags: list[str] = []
        if is_muted(name):
            tags.append(f"{DIM}(muted, advisory){RESET}")
        if is_surface(name):
            tags.append(f"{DIM}(surface — 3:1 floor){RESET}")
        tag_str = "  " + " ".join(tags) if tags else ""
        print(f"  {name:<14} {ratio:5.2f}:1   {color}{label:<9}{RESET}{tag_str}")

        if is_surface(name):
            # surface tokens just need to be distinguishable from base
            if ratio < 1.2 and name != base:
                # too close to be a useful alternate surface
                surface_warnings.append((name, ratio))
            continue
        if is_muted(name):
            continue
        if ratio < 4.5:
            failures.append((name, ratio))

    if args.pairs:
        print()
        print(f"{BOLD}all pairwise ratios{RESET}")
        print(f"{DIM}{'-' * 60}{RESET}")
        names = list(palette)
        for i, a in enumerate(names):
            for b in names[i + 1 :]:
                ratio = contrast_ratio(palette[a], palette[b])
                label, color = grade(ratio)
                print(f"  {a:<14} {DIM}<>{RESET} {b:<14} {ratio:5.2f}:1   {color}{label}{RESET}")

    print()
    if surface_warnings:
        print(f"{YELLOW}{BOLD}note{RESET}  {len(surface_warnings)} surface token(s) nearly identical to base — may not be distinguishable")
        for name, ratio in surface_warnings:
            print(f"  {YELLOW}{name}{RESET}  {ratio:.2f}:1")
    if failures:
        print(f"{RED}{BOLD}failures{RESET}  {len(failures)} foreground token(s) below AA 4.5:1 vs {base}")
        for name, ratio in failures:
            print(f"  {RED}{name}{RESET}  {ratio:.2f}:1   needs lifting")
        if args.strict:
            return 1
    else:
        print(f"{GREEN}{BOLD}pass{RESET}  all foreground tokens clear AA 4.5:1 vs {base}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
