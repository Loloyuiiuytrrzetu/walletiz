# Smar Home — Facebook ad B (joyful / colorful)

Files: `smarhome-B-9x16.mp4` (1080x1920), `smarhome-B-1x1.mp4` (1080x1080), `smarhome-B-16x9.mp4` (1920x1080). All three are 20.0 s, 30 fps, H.264 yuv420p + AAC, rendered from the same timeline (`../ad.html`, `../render.mjs`, `../music.py`).

## What I took from the reference ("numéro 2", @primalrobin / Frontier 3D, 25 s)
The reference is a cinematic 3D piece: dark Titanic → Waterloo → dinosaurs → a map of Bastogne → snowy road → a gold end card.
- **Titles live inside the scene, in 3D**: big extruded letters with depth and a drop shadow ("TITANIC" on the hull, "WATERLOO" over the battlefield, "SIEGE OF BASTOGNE" lying on the map).
- **The camera never stops pushing forward**, and at the end of a beat it **flies through the title**: the letters get huge, blur and pass the lens.
- **Zoom-blur flash cuts**: a radial streak plus a bright white/cream flash hides the cut to the next world.
- **A small subtitle pill at the bottom** (dark box, white sans text) carries the voice-over line.
- **A dotted red route on the map** shows a journey.
- **End card**: a chunky extruded colored logotype over the scene, then a small letter-spaced tagline, then one bold line with a highlighted word and an underline, then a small "↓".

How I recreated it for Smar Home, made joyful and colorful (no reference footage or branding is used):
- **Extruded titles drawn in CSS**: a stacked text-shadow gives the depth, a gradient fills the letter face, and the letters drop or rise one by one in perspective (PENSEZ MODULAIRE !, ROSÄN, MORÄN, PRIX FIXE, 7 TERRITOIRES).
- **Constant Ken Burns push** on every photo, and the title flies through the camera at the end of the hook and of each format beat.
- **Zoom-blur flash cuts** at 3.0, 8.0 and 10.0 s, using ghosted, scaled copies of the photo plus a cream flash.
- **Subtitle pills** at the bottom, kept inside the 9:16 safe area.
- **Dotted route plus pins dropping** for the 7 territories, a nod to the reference's map route.
- **End card in the same order as the reference**: the logo as a 3D tile, a letter-spaced tagline, a bold CTA button, then a small line and a bouncing "↓".
- **Added for the "joyful" brief**: tropical palette, bouncy, elastic and back easing, sticker pills, colored skewed wipes (coral/sun/turquoise), floating confetti and squiggles, camera shake on the slams, a sunburst end card with falling confetti, and a tap with ripples on "Obtenir un devis".

## Storyboard (9:16 safe area respected: nothing important in the top 8% / bottom 15%)
| Time | Beat | On screen |
|---|---|---|
| 0.0–3.0 | Hook | A coral/sun iris opens on the sunset house with palms. Sticker pills: "Envie d'une maison" / "sous les palmiers ?". The extruded 3D title "PENSEZ MODULAIRE !" drops letter by letter. Caption: "L'habitat modulaire qui change la donne dans les Caraïbes." The title flies through the camera into a zoom-blur flash. |
| 3.0–5.9 | Why modular | MORÄN pod on the beach. Pill: "Pourquoi le modulaire ?". Three slammed stamps on the beat: RAPIDE (3.5) / DURABLE (4.0) / ADAPTÉ AU CLIMAT TROPICAL (4.5). Caption: "Matériaux résistants à l'air salin, à l'humidité et aux vents." Coral/sun/turquoise wipe out. |
| 5.9–8.0 | Formats 1 | Header "Choisissez votre format". ROSÄN over the bay, then bubbles 18 m² studio / 37 m² T2 / T3 / 75 m² familial. Caption: "ROSÄN · architectural, lignes épurées, finitions premium". Fly-through, then a flash. |
| 8.0–10.0 | Formats 2 | MORÄN glass pod on the beach, then bubbles 13 m² cocon / 18 m² lodge / 25 m² 2 chambres. Caption: "MORÄN · pod futuriste, vitrage panoramique, installation express". Zoom-blur flash. |
| 10.0–13.4 | Advantages | Bright interior. "PRIX FIXE" slam with a lock sticker, "connu à l'avance", then the highlighted line "aucun dépassement" with an underline. Three chips slide in: Rapidité – Livraison et installation en un temps record · Personnalisation – Agencement et finitions selon vos désirs · Accessibilité – Espaces modernes, optimisés et confortables. Wipe out. |
| 13.4–16.5 | Zones | Lagoon-blue graphic sea. "7 TERRITOIRES" + "Caraïbes & Guyane". Pins drop on the beat along a dotted route: Saint-Martin, Guadeloupe, Marie-Galante, Dominique, Martinique, Sainte-Lucie, Guyane. A sun-yellow iris closes. |
| 16.5–20.0 | Logo + CTA | Rotating sunburst with confetti. The Smar Home logo tile drops in with a bounce. "HABITAT MODULAIRE · CARAÏBES", then badges Prix fixe / Clé en main / Personnalisable, then the pulsing button **"Obtenir un devis"** (tapped at 18.5 s with ripples). Below: "Laissez vos coordonnées, on vous rappelle" + "↓". |

No phone number, email, URL, price or website UI appears anywhere.

## Palette
Coral `#FF6B57`, sunshine `#FFC93C` (a close cousin of the brand gold), turquoise lagoon `#19C3C9`, hibiscus pink `#FF4F8B`, palm green `#2BB673`, deep navy `#0B3B66` for text and buttons, and sand/white letter faces. The gold-on-black logo is kept intact as a tile. Fonts: Baloo 2 ExtraBold (display) and Outfit (UI), stored locally in `../fonts/`.

## Music (`music.py`, original, synthesized)
- **Groove**: 120 BPM tropical / afro-house, C–G–Am–F progression with one bar per scene change. Four-on-the-floor kick, claps on 2 and 4, a swung shaker on 16ths, a conga tumbao, a bouncy off-beat bass, a pad, a steel-pan lead in a 3-3-2 soca rhythm, and marimba arpeggios from 4 s.
- **Drop**: a half-beat break at 16.0 s, then the end-card impact at 16.5 s and a sustained steel-pan chord from 18 s.
- **Sound effects synced to the picture**: an impact and pops on the hook; a pop cascade under the letter drop; whooshes into every flash and wipe; impacts on the cuts; slams on RAPIDE / DURABLE / TROPICAL, PRIX FIXE, 7 TERRITOIRES and the logo drop; pitched pops on the size bubbles; rising marimba notes on each pin drop; a click plus a bell "ding" on the CTA tap.
- **Mastering**: about -14 LUFS integrated, true peak ≤ -1.5 dBTP, 0.3 s fade-out at the end.
