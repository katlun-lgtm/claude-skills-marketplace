# Palette Recipes

Cohesive color systems with dominant + accent structure. Never an even spread across 5+ colors — pick one dominant, one supporting, one accent.

## Structure Rule

Every palette below provides:
- `--bg` — dominant surface (60-70% of pixels)
- `--surface` — secondary surface (20-25%)
- `--ink` — primary text/foreground
- `--accent` — sharp accent (5-10%, used for CTAs + highlights only)
- `--muted` — subdued text/borders

Always verify contrast — see `anti-patterns.md` for the floor.

## Recipes

### 1. Ink & Sulfur (editorial dark)
```css
--bg: #0E0E0C;
--surface: #1A1A17;
--ink: #F2EBD9;
--accent: #E4FF1A;
--muted: #6B6960;
```
Pairs with: Fraunces / Inter Tight. Mood: editorial, sharp, smart.

### 2. Bone & Oxblood (luxury warm)
```css
--bg: #F4EFE6;
--surface: #ECE4D4;
--ink: #1C0F0C;
--accent: #6B1A18;
--muted: #8C7E6A;
```
Pairs with: Cormorant / Manrope. Mood: wine, leather, old money.

### 3. Concrete & Cyan (industrial cool)
```css
--bg: #C8CAC9;
--surface: #B0B3B2;
--ink: #15171A;
--accent: #00E0D6;
--muted: #5B6066;
```
Pairs with: Archivo Narrow / Public Sans. Mood: factory, brutalist.

### 4. Cream & Cherry (playful warm)
```css
--bg: #FFF8EC;
--surface: #FFEFD0;
--ink: #2A1410;
--accent: #FF3D5A;
--muted: #A88B6B;
```
Pairs with: Lilita One / Nunito. Mood: bakery, toy-store, candy.

### 5. Forest Floor (organic dark)
```css
--bg: #1B201A;
--surface: #262C24;
--ink: #E8E5D8;
--accent: #C8A95A;
--muted: #6E7466;
```
Pairs with: Spectral / Crimson Pro. Mood: farm, ceramics, slow goods.

### 6. CRT Green (retro-future)
```css
--bg: #0A0F0B;
--surface: #121A14;
--ink: #B9FFB7;
--accent: #FF00A8;
--muted: #3D5A41;
```
Pairs with: VT323 / Space Grotesk. Mood: terminal, hacker, vaporwave.

### 7. Pearl & Storm (refined minimal)
```css
--bg: #F7F6F2;
--surface: #ECEAE3;
--ink: #14171C;
--accent: #2C4A7E;
--muted: #7F8389;
```
Pairs with: Tenor Sans / Manrope. Mood: gallery, architecture, journal.

### 8. Acid Lemon (maximalist)
```css
--bg: #FBFF38;
--surface: #F0F30A;
--ink: #1B0049;
--accent: #FF2DFB;
--muted: #5C5500;
```
Pairs with: Rubik Mono One / Anybody. Mood: rave, NFT, club.

### 9. Linen & Indigo (soft pro)
```css
--bg: #EFE9DD;
--surface: #E1D8C5;
--ink: #1A1C3A;
--accent: #3F3FFF;
--muted: #7B7560;
```
Pairs with: Fraunces / Inter Tight. Mood: SaaS-without-the-cliché.

### 10. Charcoal & Saffron (warm dark)
```css
--bg: #161413;
--surface: #221F1D;
--ink: #F1ECE3;
--accent: #F2A007;
--muted: #5F574E;
```
Pairs with: Poiret One / Forum. Mood: jazz bar, late night, theatre.

## Forbidden Combinations

- Purple gradient (`#667eea → #764ba2`) on white — the most-overused 2022 startup palette
- "Bento white" — flat white + Inter + light-gray cards (Linear/Notion clone)
- Neon teal + magenta on pure black with NO grounding neutrals
- Any palette where dominant color = `#FFFFFF` and accent = `#3B82F6` (Tailwind blue-500)

## Verifying Cohesion

Before committing a palette:
1. Render every color as a 200×200 swatch, side-by-side
2. The dominant should occupy 60-70% visual weight
3. The accent should NOT appear on any large block — only on links, CTA buttons, highlights, 1-3 hero accents
4. Muted should fade against bg (low contrast intentional, ~3:1)
5. Ink against bg must clear 7:1 (AAA) for body, 4.5:1 (AA) minimum for any text
