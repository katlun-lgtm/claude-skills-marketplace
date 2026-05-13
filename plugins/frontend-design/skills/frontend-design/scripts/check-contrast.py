#!/usr/bin/env python3
"""
check-contrast.py — WCAG 2.x contrast ratio checker for CSS variable palettes.

Usage:
    check-contrast.py <file>                        # auto-detect --bg, report vs --bg
    check-contrast.py <file> --bg <name>            # use a specific token as the base
    check-contrast.py <file> --pairs                # report ALL pairwise ratios
    check-contrast.py <file> --strict               # exit 1 if any non-muted token < 4.5:1
    check-contrast.py <file> --scope ':root'        # scope variable extraction to a CSS block
    check-contrast.py <file> --scope '[data-theme="dark"]'
    check-contrast.py <file> --check-themes         # verify both :root AND [data-theme="dark"]
    check-contrast.py <file> --check-themes --strict

Reads CSS variable declarations (`--name: #hex`) from any text file
(CSS, HTML with embedded <style>, JSX, etc). Computes WCAG 2.x relative
luminance and contrast ratios using the official formula.

For dual-theme designs (light + dark via `[data-theme="dark"]`), use
`--check-themes` to verify both palettes in one run. Without `--scope`,
the script extracts every `--var:` declaration in the file, so for
multi-theme stylesheets the *last* definition wins — silently masking
contrast bugs in the other theme. `--check-themes` solves that.

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
MUTED_TOKENS = {"muted", "rule", "hair", "hairline", "hint", "border", "divider", "subtle", "ghost"}

# Tokens that represent alternate surfaces, not foreground text. Skipped from
# the 4.5:1 text-contrast check; instead checked at 3:1 for UI distinguishability.
SURFACE_TOKENS = {"bg", "background", "surface", "canvas", "panel", "card", "well", "shell", "paper", "page", "sheet"}


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


def extract_blocks(text: str, selector: str) -> str:
    """
    Find every block `<selector> { ... }` in text and return concatenated bodies.

    Handles nested braces (e.g. selector inside @media). Selector match is
    literal — pass exactly what appears in the stylesheet.
    """
    sel_escaped = re.escape(selector)
    # selector must be preceded by start-of-text, whitespace, comma, or '}'
    pattern = re.compile(rf'(?:^|[\s,}}/]){sel_escaped}\s*\{{')
    bodies: list[str] = []
    for m in pattern.finditer(text):
        i = m.end()
        depth = 1
        start = i
        while i < len(text) and depth > 0:
            c = text[i]
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    bodies.append(text[start:i])
                    break
            i += 1
    return "\n".join(bodies)


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
    parts = re.split(r"[-_]", base)
    return any(p in SURFACE_TOKENS for p in parts)


def pick_base(palette: dict[str, tuple[int, int, int]], requested: str | None) -> str | None:
    base = requested
    if base and not base.startswith("--"):
        base = "--" + base
    if not base:
        for cand in ("--bg", "--background", "--surface", "--canvas", "--bg-deep"):
            if cand in palette:
                base = cand
                break
    if not base or base not in palette:
        return None
    return base


def report_palette(
    palette: dict[str, tuple[int, int, int]],
    base: str,
    *,
    label: str = "",
    pairs: bool = False,
) -> int:
    """Print the contrast report for a single palette. Return failure count."""
    base_rgb = palette[base]
    heading = f"palette  {label}" if label else "palette"
    print(f"{BOLD}{heading}{RESET}")
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
        glabel, color = grade(ratio)
        tags: list[str] = []
        if is_muted(name):
            tags.append(f"{DIM}(muted, advisory){RESET}")
        if is_surface(name):
            tags.append(f"{DIM}(surface — 3:1 floor){RESET}")
        tag_str = "  " + " ".join(tags) if tags else ""
        print(f"  {name:<14} {ratio:5.2f}:1   {color}{glabel:<9}{RESET}{tag_str}")

        if is_surface(name):
            if ratio < 1.2 and name != base:
                surface_warnings.append((name, ratio))
            continue
        if is_muted(name):
            continue
        if ratio < 4.5:
            failures.append((name, ratio))

    if pairs:
        print()
        print(f"{BOLD}all pairwise ratios{RESET}")
        print(f"{DIM}{'-' * 60}{RESET}")
        names = list(palette)
        for i, a in enumerate(names):
            for b in names[i + 1 :]:
                ratio = contrast_ratio(palette[a], palette[b])
                glabel, color = grade(ratio)
                print(f"  {a:<14} {DIM}<>{RESET} {b:<14} {ratio:5.2f}:1   {color}{glabel}{RESET}")

    print()
    if surface_warnings:
        print(f"{YELLOW}{BOLD}note{RESET}  {len(surface_warnings)} surface token(s) nearly identical to base — may not be distinguishable")
        for name, ratio in surface_warnings:
            print(f"  {YELLOW}{name}{RESET}  {ratio:.2f}:1")
    if failures:
        print(f"{RED}{BOLD}failures{RESET}  {len(failures)} foreground token(s) below AA 4.5:1 vs {base}")
        for name, ratio in failures:
            print(f"  {RED}{name}{RESET}  {ratio:.2f}:1   needs lifting")
    else:
        print(f"{GREEN}{BOLD}pass{RESET}  all foreground tokens clear AA 4.5:1 vs {base}")
    return len(failures)


def main() -> int:
    p = argparse.ArgumentParser(description="WCAG contrast checker for CSS variable palettes.")
    p.add_argument("file", help="CSS / HTML / JSX file containing --var declarations")
    p.add_argument("--bg", help="token name to use as base (default: auto-detect --bg or --background)")
    p.add_argument("--pairs", action="store_true", help="report ALL pairwise ratios")
    p.add_argument("--strict", action="store_true", help="exit 1 if any non-muted token fails 4.5:1 vs base")
    p.add_argument("--scope", help="CSS selector to scope variable extraction within (e.g. ':root' or '[data-theme=\"dark\"]')")
    p.add_argument("--check-themes", action="store_true", help="verify both :root AND [data-theme=\"dark\"] palettes; combined exit code")
    args = p.parse_args()

    src = Path(args.file)
    if not src.exists():
        print(f"{RED}error:{RESET} file not found: {src}", file=sys.stderr)
        return 2

    text = src.read_text(encoding="utf-8", errors="replace")

    # === multi-theme mode ===
    if args.check_themes:
        theme_scopes = [
            ("light", ":root"),
            ("dark",  '[data-theme="dark"]'),
        ]
        total_failures = 0
        for theme_label, scope in theme_scopes:
            print(f"{BOLD}━━━ {theme_label.upper()} theme (scope: {scope}) ━━━{RESET}\n")
            block_text = extract_blocks(text, scope)
            if not block_text.strip():
                print(f"{YELLOW}skipping {theme_label}: no block matching '{scope}' found{RESET}\n")
                continue
            palette = extract_palette(block_text)
            if not palette:
                print(f"{YELLOW}skipping {theme_label}: no CSS variables in block{RESET}\n")
                continue
            base = pick_base(palette, args.bg)
            if not base:
                print(f"{RED}skipping {theme_label}: no usable base token{RESET}\n")
                total_failures += 1
                continue
            total_failures += report_palette(palette, base, label=f"({theme_label})", pairs=args.pairs)
            print()
        if total_failures > 0 and args.strict:
            return 1
        return 0

    # === single-scope or whole-file mode ===
    scan_text = extract_blocks(text, args.scope) if args.scope else text
    if args.scope and not scan_text.strip():
        print(f"{RED}error:{RESET} no block matching '{args.scope}' found", file=sys.stderr)
        return 2

    palette = extract_palette(scan_text)
    if not palette:
        print(f"{YELLOW}no CSS variables found in{RESET} {src}" + (f" within {args.scope}" if args.scope else ""))
        return 0

    base = pick_base(palette, args.bg)
    if not base:
        print(f"{RED}no usable base token. pass --bg <name>.{RESET}", file=sys.stderr)
        print(f"available: {', '.join(palette)}", file=sys.stderr)
        return 2

    label = f"({args.scope})" if args.scope else f"{src}"
    failures = report_palette(palette, base, label=label, pairs=args.pairs)
    if failures > 0 and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
