# Font Pairings

Distinctive display + refined body combinations. Rotate. Never default. All available on Google Fonts unless noted.

## Pairing Recipes

### Editorial / Magazine
- **Display**: Fraunces (variable, optical sizing) — sharp serif with soft transitions
- **Body**: Inter Tight or Source Serif 4
- **When**: long-form, journalism, essay, founder letters

### Brutalist / Raw
- **Display**: Space Mono, JetBrains Mono, or IBM Plex Mono
- **Body**: same mono or Inconsolata
- **When**: dev tools, terminals, anti-design, manifestos

### Luxury / Refined
- **Display**: Cormorant Garamond, Tenor Sans, or Cardo
- **Body**: Manrope or Be Vietnam Pro at tight tracking
- **When**: jewelry, real estate, wine, watches

### Retro-Futuristic
- **Display**: VT323, Major Mono Display, or Big Shoulders Stencil
- **Body**: Space Grotesk or DM Mono
- **When**: synthwave, vaporwave, terminal aesthetic, 80s sci-fi

### Soft / Pastel
- **Display**: Caveat, Gloock, or Fraunces SOFT axis
- **Body**: Nunito or Quicksand
- **When**: wellness, kids, food, lifestyle blogs

### Industrial / Utilitarian
- **Display**: Archivo Narrow, Bebas Neue, or Antonio
- **Body**: Public Sans or Atkinson Hyperlegible
- **When**: govtech, infrastructure dashboards, logistics

### Art Deco / Geometric
- **Display**: Poiret One, Limelight, or Yeseva One
- **Body**: Josefin Sans or Forum
- **When**: theatre, hospitality, hotel sites

### Organic / Natural
- **Display**: Caudex, Spectral, or Lora italic
- **Body**: Spectral or Crimson Pro
- **When**: farm-to-table, sustainability, herbal, ceramics

### Playful / Toy-Like
- **Display**: Lilita One, Sniglet, or Bagel Fat One
- **Body**: Quicksand or Nunito
- **When**: kids products, gaming-adjacent, mascots

### Maximalist / Chaos
- **Display**: Rubik Mono One + Rubik Glitch (layer two)
- **Body**: Anybody (variable width axis), modulated
- **When**: rave flyers, NFT drops, club nights

## Forbidden Defaults

Do not use unless the brand explicitly requires it:
- Inter, Roboto, Open Sans, Lato, Montserrat
- Arial, Helvetica, system-ui
- Space Grotesk (overused 2023-2025 — only with strong justification)

## Anti-Conformity Rule

Track the last 5 pairings used in the project (commit history or a sibling `RECENT_FONTS.md`). Avoid reusing any of them for the next design. If you can't recall, pick a pairing tagged with an aesthetic NOT used recently.

## Loading

Use `<link rel="preconnect">` to fonts.googleapis.com + fonts.gstatic.com (crossorigin) before the stylesheet link. Subset to needed weights only. For variable fonts, request `wght` axis range, not discrete weights.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..900&family=Inter+Tight:wght@400;600&display=swap" rel="stylesheet">
```

Always `display=swap` — never block paint on font load.
