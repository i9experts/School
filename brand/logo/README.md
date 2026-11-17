# Adabury School: official logo files

Official logo: **Ghanta Ghar Crest**, approved as the official mark (version 1.0).
The full usage standard is in `../adabury-logo-official.html`.

| File | Use |
|---|---|
| `adabury-logo-primary.svg` | Main logo, full colour on white or linen |
| `adabury-logo-primary-on-claret.svg` | Main logo on its claret panel (gate, vans, hoardings) |
| `adabury-logo-horizontal.svg` / `-reverse.svg` | Website header, letterhead, ID cards / dark backgrounds |
| `adabury-logo-mono-claret.svg` / `-black.svg` / `-white.svg` | One-colour stamp, embroidery, engraving, photocopies, over photos |
| `adabury-crest.svg` / `-reverse.svg` | Crest alone: blazer, tie, kit, small spaces |
| `adabury-app-icon.svg` | App icon and social profile picture |
| `png/` | Transparent PNG exports (2000 px; app icon 1024 px) |

Colours: Adabury Claret `#6E1F2F`, Old Gold `#C2A15A`, Linen `#F5EEE6`, Ink `#2A1418`.
Fonts: Marcellus, Cormorant Garamond, Outfit, Noto Nastaliq Urdu (all free Google Fonts).

All lettering in the SVGs is converted to outlines. To regenerate the SVGs (e.g. after a motto change),
download Marcellus and Outfit (weight 500) as `Marcellus.ttf` and `Outfit.ttf`, then run
`pip install fonttools && python3 build_logo.py <font-folder>`.
