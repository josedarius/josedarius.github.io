# MyCloudSME — Design system ("Blueprint")

Direction: an engineering drawing come to life. Precise, calm, technical.
The motif comes straight from the logo: hexagon nodes joined by thin lines,
used as architecture diagrams. Deep navy "blueprint" sections alternate with
clean white/paper sections.

## Colours

| Token | Value | Role |
|---|---|---|
| `--navy-950` | `#06152a` | Blueprint section background |
| `--navy-900` | `#0a2240` | Cards on navy, header on scroll |
| `--navy-700` | `#16406e` | Lines on navy |
| `--blue` | `#1f8acb` | Primary brand (logo blue), links |
| `--blue-600` | `#156fa8` | Primary button background (AA on white text) |
| `--teal` | `#1baa8f` | Secondary accent, "after" states |
| `--green` | `#6cb33f` | Logo "ME" green, success / savings |
| `--ink` | `#0d1b2e` | Body text on light |
| `--muted` | `#4a5a70` | Secondary text on light |
| `--line` | `#dbe3ee` | Borders on light |
| `--paper` | `#f5f8fc` | Alternate light section |
| `--on-navy` | `#e8f0fa` | Text on navy |
| `--on-navy-muted` | `#9fb3cc` | Secondary text on navy |

Brand gradient (only for thin rules, diagram strokes and the logo mark):
`linear-gradient(90deg, #1f8acb, #1baa8f, #6cb33f)`. Never as a big background fill.

## Typography

- Headings + body: **IBM Plex Sans** (600 headings, 400 body).
- Labels, eyebrows, metrics captions, diagram labels: **IBM Plex Mono**, uppercase, 12px, letter-spacing .08em.
- Scale: 56/44/32/22/18/16/14/12. Body 17px, line-height 1.6, max 68ch.

## Spacing & shape

- 4px base; section padding 112px desktop / 72px phone.
- Container 1200px; gutters 24px.
- Radius: 6px (buttons, inputs), 10px (cards). Sharp, not bubbly.
- Shadows: almost none. Cards use 1px borders; navy cards use a 1px `--navy-700` border.
- Blueprint grid: 32px grid of 1px lines at 6% opacity on navy sections.

## Components

- **Button primary**: `--blue-600` bg, white text, 6px radius, 14px/20px padding, arrow glyph.
- **Button ghost**: transparent, 1px border in current text colour.
- **Eyebrow**: mono label with a small hexagon before it.
- **Metric**: big number (Plex Sans 600) + mono caption.
- **Case study card**: mono client/context line, title, problem → what we did → result, tag row.
- **Sample deliverable**: framed "drawing sheet" with a title block in the corner and a "SAMPLE" stamp.
- **Hex bullet**: 10px hexagon outline in teal.

## Rules

- No emoji icons. No stock photos. No invented numbers, logos or testimonials.
- Every illustrative deliverable is labelled "Sample".
- Motion: diagram lines draw in once; respect `prefers-reduced-motion`.
