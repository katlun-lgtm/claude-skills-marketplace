# Anti-Patterns

What "AI slop" looks like — and the accessibility floor every design must clear.

## AI Slop Visual Signatures

If your output matches three or more, restart the aesthetic direction:

1. **Inter / Roboto / Space Grotesk** for both headline and body
2. **Purple → blue gradient** (`#667eea → #764ba2`) on white background
3. **Single hero with centered headline + subhead + two CTAs** in identical card stack
4. **3-column feature grid** with rounded icon + 3-word label + sentence
5. **"Trusted by" logo strip** in muted gray
6. **Identical border-radius everywhere** (usually `0.5rem` or `0.75rem`)
7. **Flat tinted icons** from Lucide / Heroicons in the accent color, used decoratively
8. **Glassmorphism** (`backdrop-filter: blur(20px)` on white-translucent cards) — when overused
9. **Aurora / blurred-blob backgrounds** — 2021 dribbble cliché
10. **Bento grid clone** — uneven rectangles, soft shadows, white bg, Inter labels (Apple/Linear knockoff)

## Layout Slop

- Every section: max-width 1200px, centered, 80px vertical padding
- Every card: equal width, equal shadow, equal hover-lift (`translateY(-2px)`)
- Every hero: 50/50 split with image on right
- Every nav: logo left, 4 links center, "Get started" pill right
- Every footer: 4 columns of links + small print + social row

If you wrote any of these without questioning, you defaulted. Ship a variant first.

## Motion Slop

- Every element fades-in on scroll with `opacity: 0 → 1` and `translateY(20px → 0)`
- 0.3s ease-out on everything — no rhythm, no contrast
- Hover on every card lifts 2px and adds shadow
- Numbers in stats counting up from zero on viewport entry

Motion needs hierarchy. One hero moment + 2-3 supporting beats > everywhere-animations.

## Copy Slop

- "Empower your team to..."
- "Built for the modern..."
- "AI-powered workflow"
- "Seamlessly integrate..."
- Hero subhead = "[Product] is the [category] that helps you [verb] [noun] [adverb]"

Even if not your job to write copy, flag this when you see it. Generic copy + bold design = uncanny.

## Accessibility Floor (NON-NEGOTIABLE)

Every design must clear all of these before being marked done.

### Contrast
- **Body text vs background**: 4.5:1 minimum (WCAG AA), prefer 7:1 (AAA)
- **Large text (≥18pt or ≥14pt bold)**: 3:1 minimum
- **UI components, focus indicators, icon-only buttons**: 3:1 against adjacent colors
- Tool: paste hex pairs into `https://webaim.org/resources/contrastchecker/`

### Keyboard
- Every interactive element must be reachable via Tab in logical order
- Visible focus ring on EVERY focusable element — never `outline: none` without replacement
- Focus ring contrast ≥3:1 against background
- Skip-to-main-content link as first focusable element on full pages

### Motion
- Wrap all non-essential animation in `@media (prefers-reduced-motion: no-preference)`
- Parallax, large-distance translates, autoplay video — must respect `prefers-reduced-motion: reduce`
- Never animate more than one property per element in a single sequence unless intentional

### Semantics
- Headings in order — never skip levels (h1 → h3 without h2)
- Buttons for actions, anchors for navigation. Never `<div onclick>`.
- Form fields have `<label for>` or `aria-label`. Placeholder is NOT a label.
- Images: `alt=""` for decorative, descriptive text for content. Never alt="image" or alt="photo".

### Color Not Sole Indicator
- Error states need an icon or text marker, not just red
- Selected states need a shape change (border, weight), not just color
- Links inside body text need underline OR ≥3:1 contrast against surrounding text PLUS a hover/focus affordance

## Performance Floor

- Largest Contentful Paint < 2.5s on simulated 4G
- No layout shift after fonts load (`font-display: swap` + size-adjust)
- Total page weight (initial) < 1MB for content pages, < 200KB CSS
- No `@import` chains in CSS — one stylesheet, or `<link>` parallel loads
- Defer non-critical JS (`defer` or `type="module"`)

## Output Self-Check

Before declaring done, walk this list out loud:

1. Could you name the aesthetic in one phrase? ("Ink & Sulfur editorial dark")
2. Is there ONE unforgettable detail a viewer will remember 24 hours later?
3. Did you pick fonts NOT in the forbidden list?
4. Did you pick a palette with a clear dominant + accent (not even spread)?
5. Does at least one layout choice break the AI-slop list above?
6. Did you test keyboard tab order end-to-end?
7. Did you verify contrast on text + UI elements?
8. Does `prefers-reduced-motion: reduce` produce a sane non-animated view?
9. Did you render at 360px, 768px, and 1440px?
10. Is the code production-grade — no `console.log`, no `TODO`, no placeholder lorem outside intentional design?

Any "no" = not done.
