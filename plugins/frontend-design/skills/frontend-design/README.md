# frontend-design

A Claude Code skill for building distinctive, production-grade frontend interfaces — with bundled references and a working WCAG contrast checker.

Originated from the `frontend-design` plugin skill, hardened with the scaffolding the original lacked: concrete font/palette references, an accessibility floor, a self-check, and a contrast-verification script.

## Install

Clone into your user skills directory:

```bash
git clone <repo> ~/.claude/skills/frontend-design
```

Or copy/symlink the contents there. Claude Code auto-discovers any skill folder containing a valid `SKILL.md`.

## Structure

```
.
├── SKILL.md                          philosophy + workflow + stop criteria
├── references/
│   ├── font-pairings.md              10 aesthetics × distinctive display+body
│   ├── palette-recipes.md            10 dominant/accent palettes as CSS vars
│   └── anti-patterns.md              AI-slop signatures + a11y floor + self-check
└── scripts/
    └── check-contrast.py             WCAG 2.x contrast checker, no deps
```

## What it gives the model

1. **A named aesthetic, every time** — forces commitment before code, in one phrase.
2. **Concrete font + palette recipes** — distinctive choices that bypass Inter/Roboto/Space Grotesk defaults.
3. **A forbidden list** — slop patterns to avoid (purple-gradient-on-white, 50/50 hero, bento clones, aurora blobs).
4. **An accessibility floor** — non-negotiable: contrast, keyboard, reduced-motion, semantics.
5. **A self-check** — 10 items the model must walk through before declaring done.
6. **A verifier** — `scripts/check-contrast.py --strict` exits non-zero on AA failures so the model can't ship a 9/10 that excludes low-vision users.

## Using the contrast checker

```bash
scripts/check-contrast.py path/to/file.html              # report vs auto-detected --bg
scripts/check-contrast.py path/to/file.html --strict     # exit 1 on any failure (CI-friendly)
scripts/check-contrast.py path/to/file.html --pairs      # all pairwise ratios
scripts/check-contrast.py path/to/file.html --bg surface # use a different base token
```

The checker auto-recognises `--bg`/`--surface`/`--canvas`/`--panel` as surface tokens (3:1 floor) and `--muted`/`--rule`/`--hint` as advisory (no failure). Everything else is treated as foreground and must clear 4.5:1.

## Origin

Hardens the upstream `frontend-design` plugin skill, which was strong on philosophy but light on scaffolding. The references-plus-checker pattern earned its keep on the first test build by flagging a real AA contrast failure (`--muted` at 3.6:1) before ship — something a vibe-prompt-only skill cannot catch.
