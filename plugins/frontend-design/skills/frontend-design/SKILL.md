---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## References (read before designing)

Skim these every time — do not work from memory. They contain the concrete recipes and the floor.

- `references/font-pairings.md` — 10 distinctive display+body pairings by aesthetic, loading patterns, anti-conformity rule.
- `references/palette-recipes.md` — 10 cohesive palettes with dominant/accent structure as CSS variables, forbidden combinations, cohesion verification.
- `references/anti-patterns.md` — AI-slop visual signatures, layout slop, motion slop, copy slop, the accessibility floor (contrast/keyboard/motion/semantics), performance floor, and the final self-check.

## Scripts

- `scripts/check-contrast.py` — WCAG 2.x contrast checker. Parses `--var: #hex` declarations from any CSS/HTML/JSX file, computes pairwise ratios, flags foreground tokens that fail AA (4.5:1) against the base surface. No deps, no network.

```bash
scripts/check-contrast.py path/to/file.html              # report vs auto-detected --bg
scripts/check-contrast.py path/to/file.html --strict     # exit 1 on any failure (CI-friendly)
scripts/check-contrast.py path/to/file.html --pairs      # all pairwise ratios
scripts/check-contrast.py path/to/file.html --bg surface # use a different base token
```

Surface tokens (`--bg`, `--surface`, `--canvas`, `--panel`, …) and muted tokens (`--muted`, `--rule`, `--hint`, …) are auto-detected by name and given appropriate floors instead of the body-text 4.5:1.

## Workflow

1. **Read references** — font-pairings, palette-recipes, anti-patterns. Every time. Defaults rot otherwise.
2. **Commit to an aesthetic direction** in one phrase (e.g. "Ink & Sulfur editorial dark", "Concrete & Cyan industrial brutalism"). If you cannot name it, you have not committed.
3. **Pick fonts + palette from references** — or design new ones with the same dominant/accent discipline. Never use the forbidden lists.
4. **Identify the one unforgettable detail** — the thing a viewer will remember 24 hours later. Design around it.
5. **Implement.** Match code complexity to the aesthetic (see IMPORTANT above).
6. **Run the self-check** from `references/anti-patterns.md` (the 10-item list at the bottom). Any "no" = keep working.
7. **Run `scripts/check-contrast.py --strict`** on the output. Fix any foreground-token failures before moving on. Don't eyeball contrast.
8. **Render at 360px, 768px, 1440px** and verify the design holds at each. If you cannot render, say so explicitly — do not claim "responsive" without testing.

## Stop Criteria

The design is done when ALL of these are true:
- Aesthetic direction is nameable in one phrase
- One unforgettable detail is identifiable
- Fonts and palette are NOT on the forbidden lists
- At least one layout choice breaks the AI-slop list
- Accessibility floor (contrast, keyboard, reduced-motion, semantics) is verified — contrast confirmed via `scripts/check-contrast.py --strict` (exit 0)
- Self-check (10 items in anti-patterns.md) is fully green
- Rendered + verified at three widths (or limitation declared)

Not done = keep working. Don't ship a 6/10.