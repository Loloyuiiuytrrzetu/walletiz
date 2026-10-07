# Smar Home reel — assets found on smarhome.fr

Captured with Playwright on 2026-10-07 by `capture.mjs`. Nothing is redrawn: every UI element in the video is a crop of these captures.

## Brand (from the site CSS)
- Background `#020201`, ivory `#f9f4ee`, gold `#f3ba25`, gold gradient `135deg #f9c718 → #d79628`, border `#25211d`
- Fonts: Space Grotesk (titles, bold, tight tracking) + Inter (body), in `assets/fonts/`
- Logo: `assets/img/smar-home-logo.jpg` (gold house with "SMAR HOME / VOS RÊVES, NOTRE VISION…")
- Site copy used: "Caraïbes · Depuis 2024", "Choisissez votre modulaire", "Explorez les plans et les photos", "Assistant Smar Home — En ligne", "Zones disponibles", "Demander un devis"

## Photos (`assets/img/`)
hero-house, interior, rosan-about, rosan-bg, rosan-18-plan, rosan-18-3d, rosan-37-t2 (plan sheet), moran-13-exterior

## UI captures (`assets/ui/desktop` @1440×900 ×2, `assets/ui/mobile` @430×932 ×3)
- `hero-full`: the real homepage hero. `hero-w0..6`, `hero-eyebrow`, `header*`, `nav`, `lang`, `btn-contact`: transparent layers of the hero, used to assemble it piece by piece
- `rosan-18` → `rosan-37-hover` → `rosan-37`: real click on the "37 m²" size button on /modeles
- `lb-before` → `lb-hover` → `lb-open`: real click on the "Plan" thumbnail, which opens the lightbox
- `chat-open` → `chat-typed`: real click on "Ouvrir le chat", then real typing of "Quels sont vos délais de livraison ?"
- `zone-1..7`, `zone-star`: real "Zones disponibles" marquee words
- `adv-1..4`, `sol-1..6`, `card-rosan`, `btn-devis`, `footer-logo`
- `layout.json`: the real coordinates of every element (used to place the cursor and the zooms)
