# Quiet engineering palette trial

Classification: DEVELOPMENT appearance and packaging review.

[Overview](quiet-overview.png) · [Board before/after](board-comparison.png) · [Manufacturer reality check](manufacturer-reality-check.md).

Muted green LED, warm red power, teal filter, slate-blue amplification, dusty-violet bias and neutral-gray sense. White labels on the deep board colors; dark ink over related pale tints on warm-white card stock. This adapts the brand direction rather than claiming exact website color tokens.

Calculated sRGB label contrast: board 5.06–6.42:1; card primary ink 9.77–10.10:1, secondary ink at least 5.96:1. Black board boundaries are at least 3.27:1 against the fills. These are screen checks, not certification of printed legibility or color-vision accessibility. Labels, references, boundaries and the schematic carry meaning independently of color.

[Palette and checks](palette.json) · [Verification](verification.json) · [Board vector](quiet-06-back.svg).

[4-inch card PDF](output/pdf/quiet-engineering-retail-purchase-card.pdf) · [Bleed PDF](output/pdf/quiet-engineering-retail-purchase-card-bleed.pdf).

All board geometry and non-color PDF drawing instructions are unchanged from the earlier layouts; all 40 terminals in the independent map match the CAD netlist. No native hardware changes. Contact sheet 29, artifact 66. Previous versions preserved.

Rebuild with `build_board.py`, `build_card.py`, Poppler, `verify_palette.py` and `log_palette.py`. The supplier note is based on published specifications, not contacted-vendor approval.
