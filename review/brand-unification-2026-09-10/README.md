# PulseSensor brand unification

Classification: DEVELOPMENT appearance and packaging review, 2026-09-10.

[Unified preview](brand-overview.png) · [Board before/after](board-comparison.png) · [Review](review.html).

This iteration changes colors only, preserving the dotted-boundary board and the full-color full schematic retail purchase card layout, typography, wording, BOM, symbols and connections. The white/cream component rendering is now neutral white/gray; this is a positioning proof, not a claim about actual component material colors.

## Website palette

The palette was verified against the [live PulseSensor theme stylesheet](https://pulsesensor.com/cdn/shop/t/51/assets/theme.scss.css?v=170999498476908761131787148316) and [homepage](https://pulsesensor.com/) on 2026-09-10, with the Lab and Research pages also inspected. These are observed live website colors, not a claimed formal brand guide.

| Function | Board and card background |
| --- | --- |
| LED | Salmon #FF5A5F |
| Bias | Pale pink #FFF0F0 |
| Sense | Light gray #EEEEEE |
| Power | Gray #DADADA |
| Filter | Gray #C0C0C0 |
| Amp / gain | Gray #B3B3B3 |

Black #000000 ink and white #FFFFFF paper; secondary card text #333333. Board labels are black for contrast on the lighter backgrounds. No additional research accent was necessary. [Exact evidence excerpts](sources/palette-evidence.json) and [palette](palette.json) are saved. Full fetched public HTML/CSS is ignored by Git.

## Artifacts and validation

[Board SVG](brand-03-back.svg) · [Board PNG](brand-03-back.png).

[4-inch PDF](output/pdf/brand-full-color-full-schematic-retail-purchase-card.pdf) · [0.125-inch bleed PDF](output/pdf/brand-full-color-full-schematic-retail-purchase-card-bleed.pdf).

`verify_brand.py` checks all 40 native terminals in the independent map, PDF page/trim dimensions, and public hardware-only text. It additionally compares every board SVG geometry attribute with the prior version and all non-color PDF drawing operators with the prior card: exact matches. [Verification](verification.json).

No CAD, copper, mask, placement, optical or prior artifact files changed. Supplier-ready separations for the board remain outside this appearance iteration. Card print files retain the same dimensions.

Rebuild with `build_board.py`, `build_card.py`, Poppler, `verify_brand.py`, and `log_brand.py`. Contact sheet 26 preserves this iteration alongside the earlier alternatives.
