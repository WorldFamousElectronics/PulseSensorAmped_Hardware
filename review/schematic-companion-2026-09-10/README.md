# Complete schematic companion postcard

Classification: DEVELOPMENT packaging review proof for the JST revision. This does not promote the board to shipping-product status.

Separate two-sided 4 × 4 inch card, accompanying the [PCB, legend and reference BOM card](../postcard-insert-2026-09-10/README.md).

- Face A: complete connected circuit, organized into six numbered sections. Every chip and connector pin is explicit, including U1's three intentional no-connects. Matching labels connect between sections; B is the filter-to-amplifier connection.
- Face B: matching six-part reading guide and symbol key. Hardware only.
- Source: color-10 native schematic/netlist. All 16 components and 40 terminals (37 connected + 3 NC) checked against the independent terminal map. PDF wires were inspected visually, not extracted by an electrical connectivity engine.
- R1 is described by function; no numerical resistance is invented. Full reference BOM accompanies this on card 01.
- Vector type and schematic: 6.48 pt pin numbers, 6.72 pt component labels, 7.2 pt reading-guide body. Colors supplement labels; meaning does not depend on color alone.

## Files

[4-inch print PDF](output/pdf/PulseSensor-complete-schematic-4x4.pdf), two 288 × 288 pt pages.

[PDF with 0.125-inch bleed](output/pdf/PulseSensor-complete-schematic-4x4-bleed.pdf), two 306 × 306 pt pages with explicit 288 pt trim boxes.

[Visual review](review.html) · [Contact sheet 22](../design-contact-sheets-2026-09-09/sheet-22.png) · [Verification](verification.json).

The first layout proof is preserved in `iterations/01-complete-schematic/`. The final version fixes crowded diode/filter labels, guide line spacing, and explicitly draws U2's supply connections. Board art and first-card files are unchanged.

## Rebuild

Use the bundled Python runtime with ReportLab, pypdf and Pillow:

```
python3 build_companion.py
python3 verify_card.py
pdftoppm -scale-to 1400 -png output/pdf/PulseSensor-complete-schematic-4x4.pdf output/card
python3 log_companion.py
```
