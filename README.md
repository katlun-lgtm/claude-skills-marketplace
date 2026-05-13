# katlun-skills marketplace

Opinionated Claude Code skills with bundled references and verification scripts.

## Install

```bash
claude plugin marketplace add katlun-lgtm/claude-skills-marketplace
claude plugin install frontend-design@katlun-skills
```

## Plugins

### frontend-design

Build distinctive, production-grade frontend interfaces. Hardens the upstream `frontend-design` skill with the scaffolding it lacked:

- **References** — 10 distinctive font pairings, 10 dominant/accent palettes, AI-slop anti-patterns, and a non-negotiable accessibility floor.
- **Workflow** — forces a named aesthetic, an unforgettable detail, font/palette selection from the references, and rendering at three widths before declaring done.
- **Verifier** — `scripts/check-contrast.py --strict` computes WCAG 2.x contrast ratios from `--var: #hex` declarations and exits non-zero on AA failures. No deps, no network.

The references-plus-checker pattern earns its keep: on its first test build, the script caught a real AA contrast failure (`--muted` at 3.6:1) before ship — something a vibe-prompt-only skill cannot catch.

## Layout

```
.
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── frontend-design/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── frontend-design/
                ├── SKILL.md
                ├── README.md
                ├── references/
                │   ├── font-pairings.md
                │   ├── palette-recipes.md
                │   └── anti-patterns.md
                └── scripts/
                    └── check-contrast.py
```

## License

MIT (see individual plugins for any overrides).
