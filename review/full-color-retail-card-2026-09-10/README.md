# Full-Color Full Schematic Retail Purchase Card

Classification: DEVELOPMENT packaging review proof, JST revision.

A two-sided 4 × 4 inch card styled as a mid-century electronics assembly guide: cream paper, restrained print tints, black linework, zigzag resistor symbols, ruled headings, and a parts schedule. This is new artwork inspired by the era, not a historical document.

Face A places one continuous signal path, feedback loop and VREF connection across the six functional background hues, without separated module diagrams. Standard matching power, ground and OUT labels connect the remaining common nodes. Every component and chip/connector pin is included, including intentional U1 NC pins. Tints are lighter versions of the board module palette for black-ink readability.

Face B provides the public reference BOM and short reading guide. R1 is described by function; no resistance is invented or internal test information printed.

[Print PDF](output/pdf/full-color-full-schematic-retail-purchase-card.pdf) · [Bleed PDF](output/pdf/full-color-full-schematic-retail-purchase-card-bleed.pdf) · [Preview](output/retail-card-preview.png) · [Verification](verification.json).

Trim: 288 × 288 pt. Bleed version: 306 × 306 pt, 0.125 inch each side. Body and labels are 6.24–7.2 pt at trim size. The terminal map is checked against the native netlist; vector wiring is reviewed visually, not automatically extracted from the PDF. No native hardware or previous card was altered.

First layout retained in `iterations/01-layout/`. Rebuild with `build_card.py`, render using Poppler, validate with `verify_card.py`, and update contact sheet 25 using `log_card.py`.
